import json
import logging
from typing import Dict, List, Optional, Tuple

from chatbot import ChatBot

logger = logging.getLogger('BotFactory')


class BotFactory:
    """Factory class for creating configured chatbots with different personalities."""
    
    def __init__(self, config_file: str = 'bot_personalities.json'):
        """
        Initialize the bot factory with personality configurations.
        
        Args:
            config_file (str): Path to the JSON configuration file
        """
        self.config_file = config_file
        self.personalities = {}
        self.debate_styles = {}
        self.load_config()
    
    def load_config(self):
        """Load personality and debate style configurations from JSON file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.personalities = config.get('personalities', {})
            self.debate_styles = config.get('debate_styles', {})
            
            logger.info(f"Loaded {len(self.personalities)} personalities and {len(self.debate_styles)} debate styles")
            
        except FileNotFoundError:
            logger.error(f"Configuration file {self.config_file} not found")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in configuration file: {e}")
            raise
    
    def list_personalities(self) -> Dict[str, Dict]:
        """
        Get a dictionary of available personalities.
        
        Returns:
            Dict containing personality ID and their descriptions
        """
        return {
            pid: {
                'name': data['name'],
                'description': data['description']
            }
            for pid, data in self.personalities.items()
        }
    
    def list_debate_styles(self) -> Dict[str, Dict]:
        """
        Get a dictionary of available debate styles.
        
        Returns:
            Dict containing debate style ID and their descriptions
        """
        return self.debate_styles
    
    def create_bot(self, 
                   name: str,
                   topic: str, 
                   position: str,
                   personality: str = 'balanced',
                   debate_style: str = 'casual',
                   output_file: Optional[str] = None) -> ChatBot:
        """
        Create a chatbot with specified personality and configuration.
        
        Args:
            name (str): Name for the bot
            topic (str): The debate topic
            position (str): The position this bot will support
            personality (str): Personality type from config
            debate_style (str): Debate style from config
            output_file (str): Optional output file for bot responses
        
        Returns:
            Configured ChatBot instance
        """
        if personality not in self.personalities:
            available = list(self.personalities.keys())
            raise ValueError(f"Unknown personality '{personality}'. Available: {available}")
        
        if debate_style not in self.debate_styles:
            available = list(self.debate_styles.keys())
            raise ValueError(f"Unknown debate style '{debate_style}'. Available: {available}")
        
        personality_config = self.personalities[personality]
        style_config = self.debate_styles[debate_style]
        
        # Create system prompt combining personality and topic
        system_content = f"{personality_config['system_prompt']} The topic is: {topic}. You support the position that {position}. {style_config['format']}"
        
        config = [{
            "role": "system",
            "content": system_content
        }]
        
        # Create bot with optional output file
        bot_output = output_file if output_file else f"{name.lower()}_responses.txt"
        bot = ChatBot(name, output=bot_output)
        bot.create_role(config)
        
        logger.info(f"Created bot '{name}' with personality '{personality}' supporting '{position}'")
        
        return bot
    
    def create_debate_pair(self,
                          topic: str,
                          position1: str, 
                          position2: str,
                          bot1_name: str = "Bot1",
                          bot2_name: str = "Bot2",
                          personality1: str = 'emotional',
                          personality2: str = 'logical',
                          debate_style: str = 'casual') -> Tuple[ChatBot, ChatBot]:
        """
        Create a pair of bots with complementary personalities for debating.
        
        Args:
            topic (str): The debate topic
            position1 (str): Position for first bot
            position2 (str): Position for second bot
            bot1_name (str): Name for first bot
            bot2_name (str): Name for second bot
            personality1 (str): Personality for first bot
            personality2 (str): Personality for second bot
            debate_style (str): Debate style for both bots
        
        Returns:
            Tuple of (bot1, bot2)
        """
        bot1 = self.create_bot(bot1_name, topic, position1, personality1, debate_style)
        bot2 = self.create_bot(bot2_name, topic, position2, personality2, debate_style)
        
        return bot1, bot2
    
    def get_opening_prompt(self, debate_style: str = 'casual') -> str:
        """
        Get the opening prompt for a specific debate style.
        
        Args:
            debate_style (str): The debate style
            
        Returns:
            Opening prompt string
        """
        if debate_style not in self.debate_styles:
            debate_style = 'casual'
        
        return self.debate_styles[debate_style]['opening_prompt']
    
    def add_personality(self, 
                       personality_id: str,
                       name: str,
                       description: str,
                       system_prompt: str,
                       save_to_file: bool = True):
        """
        Add a new personality to the configuration.
        
        Args:
            personality_id (str): Unique identifier for the personality
            name (str): Display name for the personality
            description (str): Description of the personality
            system_prompt (str): System prompt template for this personality
            save_to_file (bool): Whether to save to the config file
        """
        self.personalities[personality_id] = {
            'name': name,
            'description': description,
            'system_prompt': system_prompt
        }
        
        if save_to_file:
            self.save_config()
        
        logger.info(f"Added new personality: {personality_id}")
    
    def save_config(self):
        """Save current configuration to file."""
        config = {
            'personalities': self.personalities,
            'debate_styles': self.debate_styles
        }
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            logger.error(f"Failed to save configuration: {e}")
            raise


# Convenience functions for backward compatibility
def create_debate_bots(topic: str, 
                      position1: str, 
                      position2: str, 
                      bot1_name: str = "Bot1", 
                      bot2_name: str = "Bot2",
                      personality1: str = 'emotional',
                      personality2: str = 'logical',
                      debate_style: str = 'casual') -> Tuple[ChatBot, ChatBot]:
    """
    Convenience function to create debate bots using the factory.
    """
    factory = BotFactory()
    return factory.create_debate_pair(
        topic, position1, position2, 
        bot1_name, bot2_name, 
        personality1, personality2, 
        debate_style
    )


def list_available_personalities() -> Dict[str, Dict]:
    """
    Convenience function to list available personalities.
    """
    factory = BotFactory()
    return factory.list_personalities()


def list_available_debate_styles() -> Dict[str, Dict]:
    """
    Convenience function to list available debate styles.
    """
    factory = BotFactory()
    return factory.list_debate_styles()


if __name__ == "__main__":
    # Example usage and testing
    factory = BotFactory()
    
    print("Available Personalities:")
    for pid, info in factory.list_personalities().items():
        print(f"  {pid}: {info['name']} - {info['description']}")
    
    print("\nAvailable Debate Styles:")
    for style_id, style_info in factory.list_debate_styles().items():
        print(f"  {style_id}: {style_info['opening_prompt']}")
    
    # Create a sample bot
    bot = factory.create_bot(
        name="TestBot",
        topic="Should AI be regulated?",
        position="AI should be heavily regulated",
        personality="logical",
        debate_style="formal"
    )
    
    print(f"\nCreated bot: {bot.name}")