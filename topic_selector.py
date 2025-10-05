#!/usr/bin/env python3
"""
Topic selection module for FightBot.
Handles all topic-related functionality including management, selection, and user interaction.
"""

import json
import logging
import os
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger('TopicSelector')


class TopicManager:
    """Manages debate topics from file or user input."""
    
    def __init__(self, topics_file: str = 'debate_topics.json'):
        self.topics_file = topics_file
        self.topics = {}
        self.logger = logging.getLogger('TopicManager')
        self.load_topics()
    
    def load_topics(self):
        """Load topics from JSON file."""
        try:
            with open(self.topics_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.topics = {topic['id']: topic for topic in data.get('debate_topics', [])}
            self.logger.info(f"Loaded {len(self.topics)} debate topics from {self.topics_file}")
            
        except FileNotFoundError:
            self.logger.warning(f"Topics file {self.topics_file} not found. Using empty topic list.")
            self.topics = {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in topics file: {e}")
            self.topics = {}
    
    def list_topics(self, category: str = None, difficulty: str = None) -> Dict[str, Dict]:
        """Get filtered list of available topics."""
        filtered_topics = {}
        
        for topic_id, topic_data in self.topics.items():
            if category and topic_data.get('category', '').lower() != category.lower():
                continue
            if difficulty and topic_data.get('difficulty', '').lower() != difficulty.lower():
                continue
            
            filtered_topics[topic_id] = topic_data
        
        return filtered_topics
    
    def get_topic(self, topic_id: str) -> Optional[Dict]:
        """Get a specific topic by ID."""
        return self.topics.get(topic_id)
    
    def get_categories(self) -> List[str]:
        """Get all available topic categories."""
        categories = set()
        for topic in self.topics.values():
            if 'category' in topic:
                categories.add(topic['category'])
        return sorted(list(categories))
    
    def get_difficulties(self) -> List[str]:
        """Get all available difficulty levels."""
        difficulties = set()
        for topic in self.topics.values():
            if 'difficulty' in topic:
                difficulties.add(topic['difficulty'])
        return sorted(list(difficulties))
    
    def add_topic(self, topic_id: str, topic: str, position1: str, position2: str, 
                  category: str = "Custom", difficulty: str = "intermediate", 
                  description: str = "", save_to_file: bool = True) -> Dict:
        """Add a new topic."""
        new_topic = {
            'id': topic_id,
            'topic': topic,
            'position1': position1,
            'position2': position2,
            'category': category,
            'difficulty': difficulty,
            'description': description
        }
        
        self.topics[topic_id] = new_topic
        
        if save_to_file:
            self.save_topics()
        
        self.logger.info(f"Added new topic: {topic_id}")
        return new_topic
    
    def save_topics(self):
        """Save topics to JSON file."""
        try:
            data = {'debate_topics': list(self.topics.values())}
            
            with open(self.topics_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Saved {len(self.topics)} topics to {self.topics_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save topics: {e}")
    
    def display_topics(self, topics: Dict[str, Dict] = None, show_details: bool = False):
        """Display topics in a formatted way."""
        if topics is None:
            topics = self.topics
        
        if not topics:
            print("No topics available.")
            return
        
        print("\\nAvailable Debate Topics:")
        print("=" * 50)
        
        for i, (topic_id, topic_data) in enumerate(topics.items(), 1):
            category = topic_data.get('category', 'Unknown')
            difficulty = topic_data.get('difficulty', 'Unknown')
            
            print(f"{i:2d}. [{category}] {topic_data['topic']}")
            
            if show_details:
                print(f"    Difficulty: {difficulty.title()}")
                print(f"    Position A: {topic_data['position1']}")
                print(f"    Position B: {topic_data['position2']}")
                if topic_data.get('description'):
                    print(f"    Description: {topic_data['description']}")
            else:
                print(f"    ({difficulty} difficulty)")
            
            print()


class TopicSelector:
    """Handles topic selection user interface and interaction."""
    
    def __init__(self, topic_manager: TopicManager = None):
        self.topic_manager = topic_manager or TopicManager()
        self.logger = logging.getLogger('TopicSelector')
    
    def get_input_mode(self) -> str:
        """Ask user to choose between file mode and interactive mode."""
        logger = logging.getLogger("ModeSelection")
        
        print("\\n=== Input Mode Selection ===")
        print("1. File Mode - Choose from predefined topics")
        print("2. Interactive Mode - Enter your own topic manually")
        print("3. Browse Mode - Browse topics by category or search")
        
        while True:
            try:
                choice = input("\\nSelect input mode (1-3): ").strip()
                
                if choice == '1':
                    logger.info("User selected file mode")
                    return 'file'
                elif choice == '2':
                    logger.info("User selected interactive mode")
                    return 'interactive'
                elif choice == '3':
                    logger.info("User selected browse mode")
                    return 'browse'
                else:
                    print("Invalid choice. Please enter 1, 2, or 3.")
                    
            except KeyboardInterrupt:
                logger.info("Mode selection cancelled by user")
                raise
            except Exception as e:
                logger.error(f"Error in mode selection: {e}")
                print(f"Error: {e}. Please try again.")
    
    def get_topic_from_file(self) -> Tuple[str, str, str]:
        """Get topic from predefined file topics with simple selection."""
        logger = logging.getLogger("FileMode")
        
        topics = self.topic_manager.list_topics()
        
        if not topics:
            logger.warning("No predefined topics available, falling back to interactive mode")
            print("\\nNo predefined topics available. Please enter a custom topic.")
            return self.get_topic_interactive()
        
        print("\\n=== Available Topics ===")
        self.topic_manager.display_topics(topics)
        
        topic_ids = list(topics.keys())
        
        while True:
            try:
                choice = input(f"\\nChoose topic (1-{len(topic_ids)}): ").strip()
                
                idx = int(choice) - 1
                if 0 <= idx < len(topic_ids):
                    selected_topic = topics[topic_ids[idx]]
                    logger.info(f"Selected predefined topic: {selected_topic['id']}")
                    return selected_topic['topic'], selected_topic['position1'], selected_topic['position2']
                else:
                    print(f"Please enter a number between 1 and {len(topic_ids)}")
                    
            except ValueError:
                print("Invalid input. Please enter a number.")
            except KeyboardInterrupt:
                logger.info("File topic selection cancelled")
                raise
    
    def get_topic_interactive(self) -> Tuple[str, str, str]:
        """Get topic through interactive manual input."""
        logger = logging.getLogger("InteractiveMode")
        
        print("\\n=== Interactive Topic Entry ===")
        
        topic = input("\\nEnter the debate topic: ").strip()
        while not topic:
            topic = input("Please enter a valid topic: ").strip()
        
        position1 = input(f"\\nEnter the first position on '{topic}': ").strip()
        while not position1:
            position1 = input("Please enter a valid first position: ").strip()
        
        position2 = input(f"\\nEnter the opposing position on '{topic}': ").strip()
        while not position2:
            position2 = input("Please enter a valid opposing position: ").strip()
        
        logger.info("User created custom topic interactively")
        return topic, position1, position2
    
    def get_topic_from_browse_mode(self) -> Tuple[str, str, str]:
        """Get topic selection from user with browsing options."""
        logger = logging.getLogger("BrowseMode")
        
        print("\\n=== Browse Topics ===")
        print("1. View all topics")
        print("2. Browse by category")
        print("3. Browse by difficulty")
        print("4. Search topics")
        print("5. Enter custom topic")
        
        while True:
            try:
                choice = input("\\nSelect option (1-5): ").strip()
                
                if choice == '1':
                    return self.select_predefined_topic()
                elif choice == '2':
                    return self.browse_topics_by_category()
                elif choice == '3':
                    return self.browse_topics_by_difficulty()
                elif choice == '4':
                    return self.search_topics()
                elif choice == '5':
                    return self.create_custom_topic()
                else:
                    print("Invalid choice. Please enter 1-5.")
                    
            except KeyboardInterrupt:
                logger.info("Browse mode cancelled by user")
                raise
            except Exception as e:
                logger.error(f"Error in browse mode: {e}")
                print(f"Error: {e}. Please try again.")
    
    def select_predefined_topic(self) -> Tuple[str, str, str]:
        """Select from available predefined topics."""
        topics = self.topic_manager.list_topics()
        
        if not topics:
            print("\\nNo predefined topics available. Please enter a custom topic.")
            return self.create_custom_topic()
        
        self.topic_manager.display_topics(topics)
        
        topic_ids = list(topics.keys())
        
        while True:
            try:
                choice = input(f"\\nChoose topic (1-{len(topic_ids)}) or 'c' for custom: ").strip()
                
                if choice.lower() == 'c':
                    return self.create_custom_topic()
                
                idx = int(choice) - 1
                if 0 <= idx < len(topic_ids):
                    selected_topic = topics[topic_ids[idx]]
                    return selected_topic['topic'], selected_topic['position1'], selected_topic['position2']
                else:
                    print(f"Please enter a number between 1 and {len(topic_ids)}")
                    
            except ValueError:
                print("Invalid input. Please enter a number or 'c' for custom.")
            except KeyboardInterrupt:
                raise
    
    def browse_topics_by_category(self) -> Tuple[str, str, str]:
        """Browse topics filtered by category."""
        categories = self.topic_manager.get_categories()
        
        if not categories:
            print("\\nNo categories available. Showing all topics.")
            return self.select_predefined_topic()
        
        print("\\nAvailable Categories:")
        for i, category in enumerate(categories, 1):
            topic_count = len(self.topic_manager.list_topics(category=category))
            print(f"  {i}. {category} ({topic_count} topics)")
        
        while True:
            try:
                choice = input(f"\\nChoose category (1-{len(categories)}) or 'a' for all: ").strip()
                
                if choice.lower() == 'a':
                    return self.select_predefined_topic()
                
                idx = int(choice) - 1
                if 0 <= idx < len(categories):
                    selected_category = categories[idx]
                    filtered_topics = self.topic_manager.list_topics(category=selected_category)
                    
                    print(f"\\nTopics in {selected_category}:")
                    self.topic_manager.display_topics(filtered_topics, show_details=True)
                    
                    topic_ids = list(filtered_topics.keys())
                    
                    topic_choice = input(f"\\nChoose topic (1-{len(topic_ids)}): ").strip()
                    topic_idx = int(topic_choice) - 1
                    
                    if 0 <= topic_idx < len(topic_ids):
                        selected_topic = filtered_topics[topic_ids[topic_idx]]
                        return selected_topic['topic'], selected_topic['position1'], selected_topic['position2']
                    else:
                        print(f"Please enter a number between 1 and {len(topic_ids)}")
                else:
                    print(f"Please enter a number between 1 and {len(categories)}")
                    
            except ValueError:
                print("Invalid input. Please enter a number or 'a' for all.")
            except KeyboardInterrupt:
                raise
    
    def browse_topics_by_difficulty(self) -> Tuple[str, str, str]:
        """Browse topics filtered by difficulty level."""
        difficulties = self.topic_manager.get_difficulties()
        
        if not difficulties:
            print("\\nNo difficulty levels available. Showing all topics.")
            return self.select_predefined_topic()
        
        print("\\nAvailable Difficulty Levels:")
        for i, difficulty in enumerate(difficulties, 1):
            topic_count = len(self.topic_manager.list_topics(difficulty=difficulty))
            print(f"  {i}. {difficulty.title()} ({topic_count} topics)")
        
        while True:
            try:
                choice = input(f"\\nChoose difficulty (1-{len(difficulties)}) or 'a' for all: ").strip()
                
                if choice.lower() == 'a':
                    return self.select_predefined_topic()
                
                idx = int(choice) - 1
                if 0 <= idx < len(difficulties):
                    selected_difficulty = difficulties[idx]
                    filtered_topics = self.topic_manager.list_topics(difficulty=selected_difficulty)
                    
                    print(f"\\nTopics with {selected_difficulty} difficulty:")
                    self.topic_manager.display_topics(filtered_topics, show_details=True)
                    
                    topic_ids = list(filtered_topics.keys())
                    
                    topic_choice = input(f"\\nChoose topic (1-{len(topic_ids)}): ").strip()
                    topic_idx = int(topic_choice) - 1
                    
                    if 0 <= topic_idx < len(topic_ids):
                        selected_topic = filtered_topics[topic_ids[topic_idx]]
                        return selected_topic['topic'], selected_topic['position1'], selected_topic['position2']
                    else:
                        print(f"Please enter a number between 1 and {len(topic_ids)}")
                else:
                    print(f"Please enter a number between 1 and {len(difficulties)}")
                    
            except ValueError:
                print("Invalid input. Please enter a number or 'a' for all.")
            except KeyboardInterrupt:
                raise
    
    def search_topics(self) -> Tuple[str, str, str]:
        """Search topics by keyword and select from results."""
        search_term = input("\\nEnter search term: ").strip().lower()
        
        if not search_term:
            print("No search term entered. Showing all topics.")
            return self.select_predefined_topic()
        
        matches = {}
        for tid, tdata in self.topic_manager.topics.items():
            if (search_term in tdata.get('topic', '').lower() or 
                search_term in tdata.get('position1', '').lower() or 
                search_term in tdata.get('position2', '').lower() or 
                search_term in tdata.get('description', '').lower() or 
                search_term in tdata.get('category', '').lower()):
                matches[tid] = tdata
        
        if not matches:
            print(f"\\nNo topics found matching '{search_term}'. Try a different search term.")
            return self.search_topics()
        
        print(f"\\nFound {len(matches)} topics matching '{search_term}':")
        self.topic_manager.display_topics(matches, show_details=True)
        
        topic_ids = list(matches.keys())
        
        while True:
            try:
                choice = input(f"\\nChoose topic (1-{len(topic_ids)}) or 's' to search again: ").strip()
                
                if choice.lower() == 's':
                    return self.search_topics()
                
                idx = int(choice) - 1
                if 0 <= idx < len(topic_ids):
                    selected_topic = matches[topic_ids[idx]]
                    return selected_topic['topic'], selected_topic['position1'], selected_topic['position2']
                else:
                    print(f"Please enter a number between 1 and {len(topic_ids)}")
                    
            except ValueError:
                print("Invalid input. Please enter a number or 's' to search again.")
            except KeyboardInterrupt:
                raise
    
    def create_custom_topic(self) -> Tuple[str, str, str]:
        """Create a custom debate topic."""
        logger = logging.getLogger("CustomTopic")
        
        print("\\n=== Create Custom Topic ===")
        
        topic = input("\\nEnter the debate topic: ").strip()
        while not topic:
            topic = input("Please enter a valid topic: ").strip()
        
        position1 = input(f"\\nEnter the first position on '{topic}': ").strip()
        while not position1:
            position1 = input("Please enter a valid first position: ").strip()
        
        position2 = input(f"\\nEnter the opposing position on '{topic}': ").strip()
        while not position2:
            position2 = input("Please enter a valid opposing position: ").strip()
        
        # Optional: save custom topic
        save_topic = input("\\nSave this topic for future use? (y/N): ").strip().lower()
        if save_topic == 'y':
            try:
                topic_id = topic.lower().replace(' ', '_').replace('?', '').replace('!', '')
                topic_id = ''.join(c for c in topic_id if c.isalnum() or c == '_')[:50]
                
                category = input("Category (default: Custom): ").strip() or "Custom"
                difficulty = input("Difficulty (beginner/intermediate/advanced, default: intermediate): ").strip() or "intermediate"
                description = input("Description (optional): ").strip()
                
                self.topic_manager.add_topic(topic_id, topic, position1, position2, category, difficulty, description)
                logger.info(f"Saved custom topic: {topic_id}")
                print(f"Topic saved as '{topic_id}'")
                
            except Exception as e:
                logger.error(f"Failed to save custom topic: {e}")
                print(f"Warning: Could not save topic: {e}")
        
        return topic, position1, position2
    
    def get_topic_selection(self) -> Tuple[str, str, str, str]:
        """Main entry point for topic selection. Returns topic, position1, position2, and mode."""
        # Get input mode preference
        mode = self.get_input_mode()
        self.logger.info(f"Selected input mode: {mode}")
        
        # Get topic based on selected mode
        if mode == 'file':
            topic, position1, position2 = self.get_topic_from_file()
        elif mode == 'interactive':
            topic, position1, position2 = self.get_topic_interactive()
        else:  # browse mode
            topic, position1, position2 = self.get_topic_from_browse_mode()
        
        self.logger.info(f"Selected topic: {topic}")
        self.logger.info(f"Position 1: {position1}")
        self.logger.info(f"Position 2: {position2}")
        
        return topic, position1, position2, mode
    
    def offer_topic_saving(self, topic: str, position1: str, position2: str) -> bool:
        """Offer to save a custom topic after debate completion."""
        save_choice = input("\\n\\nWould you like to save this topic for future use? (y/N): ").strip().lower()
        if save_choice == 'y':
            try:
                topic_id = topic.lower().replace(' ', '_').replace('?', '').replace('!', '')
                topic_id = ''.join(c for c in topic_id if c.isalnum() or c == '_')[:50]
                
                category = input("Category (default: Custom): ").strip() or "Custom"
                difficulty = input("Difficulty (beginner/intermediate/advanced, default: intermediate): ").strip() or "intermediate"
                description = input("Description (optional): ").strip()
                
                self.topic_manager.add_topic(topic_id, topic, position1, position2, category, difficulty, description)
                print(f"Topic saved as '{topic_id}'")
                self.logger.info(f"User saved debate topic: {topic_id}")
                return True
                
            except Exception as e:
                self.logger.error(f"Failed to save topic: {e}")
                print(f"Warning: Could not save topic: {e}")
                return False
        return False


def manage_topics():
    """Interactive topic management utility."""
    topic_manager = TopicManager()
    logger = logging.getLogger("TopicManager")
    
    while True:
        print("\\n=== Topic Management ===")
        print("1. List all topics")
        print("2. Add new topic")
        print("3. Browse by category")
        print("4. Browse by difficulty")
        print("5. Search topics")
        print("6. Exit")
        
        try:
            choice = input("\\nSelect option (1-6): ").strip()
            
            if choice == '1':
                topic_manager.display_topics(show_details=True)
                
            elif choice == '2':
                print("\\n=== Add New Topic ===")
                topic_id = input("Topic ID (unique identifier): ").strip()
                if topic_id in topic_manager.topics:
                    print(f"Topic '{topic_id}' already exists.")
                    continue
                
                topic = input("Topic question: ").strip()
                position1 = input("Position 1: ").strip()
                position2 = input("Position 2: ").strip()
                category = input("Category: ").strip()
                difficulty = input("Difficulty (beginner/intermediate/advanced): ").strip()
                description = input("Description: ").strip()
                
                topic_manager.add_topic(topic_id, topic, position1, position2, category, difficulty, description)
                print(f"Added topic '{topic_id}'")
                
            elif choice == '3':
                categories = topic_manager.get_categories()
                if categories:
                    print("\\nCategories:")
                    for i, cat in enumerate(categories, 1):
                        print(f"  {i}. {cat}")
                    
                    cat_choice = input(f"\\nChoose category (1-{len(categories)}): ").strip()
                    try:
                        idx = int(cat_choice) - 1
                        if 0 <= idx < len(categories):
                            selected_cat = categories[idx]
                            filtered = topic_manager.list_topics(category=selected_cat)
                            topic_manager.display_topics(filtered, show_details=True)
                    except ValueError:
                        print("Invalid choice.")
                else:
                    print("No categories found.")
                    
            elif choice == '4':
                difficulties = topic_manager.get_difficulties()
                if difficulties:
                    print("\\nDifficulties:")
                    for i, diff in enumerate(difficulties, 1):
                        print(f"  {i}. {diff.title()}")
                    
                    diff_choice = input(f"\\nChoose difficulty (1-{len(difficulties)}): ").strip()
                    try:
                        idx = int(diff_choice) - 1
                        if 0 <= idx < len(difficulties):
                            selected_diff = difficulties[idx]
                            filtered = topic_manager.list_topics(difficulty=selected_diff)
                            topic_manager.display_topics(filtered, show_details=True)
                    except ValueError:
                        print("Invalid choice.")
                else:
                    print("No difficulty levels found.")
                    
            elif choice == '5':
                search_term = input("\\nEnter search term: ").strip().lower()
                if search_term:
                    matches = {}
                    for tid, tdata in topic_manager.topics.items():
                        if (search_term in tdata.get('topic', '').lower() or 
                            search_term in tdata.get('position1', '').lower() or 
                            search_term in tdata.get('position2', '').lower() or 
                            search_term in tdata.get('description', '').lower()):
                            matches[tid] = tdata
                    
                    if matches:
                        print(f"\\nFound {len(matches)} matching topics:")
                        topic_manager.display_topics(matches, show_details=True)
                    else:
                        print("No matching topics found.")
                        
            elif choice == '6':
                logger.info("Topic management session ended")
                break
                
            else:
                print("Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            logger.info("Topic management interrupted")
            break
        except Exception as e:
            logger.error(f"Error in topic management: {e}")
            print(f"Error: {e}")


# Convenience functions for backward compatibility
def get_topic_selection() -> Tuple[str, str, str, str]:
    """Convenience function to get topic selection using the TopicSelector."""
    selector = TopicSelector()
    return selector.get_topic_selection()


if __name__ == "__main__":
    # Example usage
    selector = TopicSelector()
    topic, pos1, pos2, mode = selector.get_topic_selection()
    print(f"\\nSelected: {topic}")
    print(f"Position 1: {pos1}")
    print(f"Position 2: {pos2}")
    print(f"Mode: {mode}")