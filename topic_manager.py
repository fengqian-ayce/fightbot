#!/usr/bin/env python3
"""
Topic management utility for FightBot.
Standalone script to manage debate topics without running full debates.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from topic_selector import TopicManager, manage_topics


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] in ['-h', '--help', 'help']:
            show_topic_help()
            return
        elif sys.argv[1] == 'list':
            list_topics()
            return
        elif sys.argv[1] == 'categories':
            show_categories()
            return
        elif sys.argv[1] == 'difficulties':
            show_difficulties()
            return
    
    # Run interactive topic manager
    manage_topics()


def show_topic_help():
    """Show help for topic management."""
    print("=== FightBot Topic Manager Help ===")
    print()
    print("Usage:")
    print("  python topic_manager.py           - Interactive topic management")
    print("  python topic_manager.py list     - List all available topics")
    print("  python topic_manager.py categories - Show topics by category")
    print("  python topic_manager.py difficulties - Show topics by difficulty")
    print("  python topic_manager.py help     - Show this help message")
    print()
    print("Interactive Mode Commands:")
    print("  1. List all topics - View all available debate topics")
    print("  2. Add new topic - Create and save a new debate topic")
    print("  3. Browse by category - Filter topics by subject area")
    print("  4. Browse by difficulty - Filter topics by complexity level")
    print("  5. Search topics - Find topics by keyword")
    print("  6. Exit - Close the topic manager")


def list_topics():
    """List all available topics."""
    topic_manager = TopicManager()
    
    if not topic_manager.topics:
        print("No topics available.")
        return
    
    print(f"=== All Available Topics ({len(topic_manager.topics)} total) ===")
    topic_manager.display_topics(show_details=True)


def show_categories():
    """Show topics organized by category."""
    topic_manager = TopicManager()
    categories = topic_manager.get_categories()
    
    if not categories:
        print("No categories found.")
        return
    
    print("=== Topics by Category ===")
    for category in categories:
        topics = topic_manager.list_topics(category=category)
        print(f"\n{category.upper()} ({len(topics)} topics)")
        print("-" * (len(category) + 10))
        
        for topic_id, topic_data in topics.items():
            difficulty = topic_data.get('difficulty', 'unknown').title()
            print(f"  [{difficulty}] {topic_data['topic']}")
            print(f"    Pro: {topic_data['position1']}")
            print(f"    Con: {topic_data['position2']}")
            if topic_data.get('description'):
                print(f"    Description: {topic_data['description']}")
            print()


def show_difficulties():
    """Show topics organized by difficulty."""
    topic_manager = TopicManager()
    difficulties = topic_manager.get_difficulties()
    
    if not difficulties:
        print("No difficulty levels found.")
        return
    
    print("=== Topics by Difficulty ===")
    for difficulty in difficulties:
        topics = topic_manager.list_topics(difficulty=difficulty)
        print(f"\n{difficulty.upper()} ({len(topics)} topics)")
        print("-" * (len(difficulty) + 10))
        
        for topic_id, topic_data in topics.items():
            category = topic_data.get('category', 'Unknown')
            print(f"  [{category}] {topic_data['topic']}")
            print(f"    Pro: {topic_data['position1']}")
            print(f"    Con: {topic_data['position2']}")
            if topic_data.get('description'):
                print(f"    Description: {topic_data['description']}")
            print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nTopic manager closed.")
    except Exception as e:
        print(f"Error: {e}")