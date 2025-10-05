#!/usr/bin/env python3
"""
Example script demonstrating the FightBot personality system.
"""

import logging
import tempfile
import os
from datetime import datetime

from bot_factory import BotFactory, list_available_personalities, list_available_debate_styles
from chatbot import start_debate

# Setup logging for examples
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

example_logger = logging.getLogger("FightBotExample")


def quick_demo():
    """Quick demo with predefined setup."""
    example_logger.info("=== FightBot Quick Demo ===")
    print("=== FightBot Quick Demo ===")
    
    factory = BotFactory()
    
    # Create bots with different personalities for a climate change debate
    topic = "Should governments prioritize economic growth or environmental protection?"
    position1 = "Economic growth should be the priority"
    position2 = "Environmental protection should be the priority"
    
    example_logger.info(f"Topic: {topic}")
    example_logger.info(f"Position 1 (Populist): {position1}")
    example_logger.info(f"Position 2 (Academic): {position2}")
    
    print(f"Topic: {topic}")
    print(f"Position 1 (Populist): {position1}")
    print(f"Position 2 (Academic): {position2}")
    
    bot1, bot2 = factory.create_debate_pair(
        topic=topic,
        position1=position1,
        position2=position2,
        bot1_name="EconomyFirst",
        bot2_name="GreenAdvocate", 
        personality1="populist",    # Appeals to common people
        personality2="academic",    # Uses scholarly approach
        debate_style="town_hall"    # Community meeting format
    )
    
    # Start a 3-round debate
    opening = factory.get_opening_prompt("town_hall")
    start_debate(bot1, bot2, initial_prompt=opening, max_rounds=3)


def personality_showcase():
    """Show all available personalities and their characteristics."""
    example_logger.info("=== Available Bot Personalities ===")
    print("=== Available Bot Personalities ===")
    
    personalities = list_available_personalities()
    for i, (pid, info) in enumerate(personalities.items(), 1):
        personality_details = f"{i}. {pid.upper()} - {info['name']}: {info['description']}"
        example_logger.info(personality_details)
        
        print(f"\n{i}. {pid.upper()}")
        print(f"   Name: {info['name']}")
        print(f"   Description: {info['description']}")
    
    example_logger.info("=== Available Debate Styles ===")
    print("\n=== Available Debate Styles ===")
    
    styles = list_available_debate_styles()
    for i, (sid, info) in enumerate(styles.items(), 1):
        style_details = f"{i}. {sid.upper()} - Opening: {info['opening_prompt']}, Format: {info['format']}"
        example_logger.info(style_details)
        
        print(f"\n{i}. {sid.upper()}")
        print(f"   Opening: {info['opening_prompt']}")
        print(f"   Format: {info['format']}")


def custom_personality_demo():
    """Demonstrate adding a custom personality."""
    example_logger.info("=== Custom Personality Demo ===")
    print("=== Custom Personality Demo ===")
    
    factory = BotFactory()
    
    # Add a new personality
    factory.add_personality(
        personality_id="sarcastic",
        name="Sarcastic Commentator", 
        description="Uses wit, sarcasm, and humor to make points",
        system_prompt="Act like a sarcastic political commentator in a debate. Use wit, irony, and humor to make your points. Be clever with your sarcasm but still make substantive arguments. Don't be mean-spirited, just cleverly sarcastic.",
        save_to_file=False  # Don't save to avoid modifying the config
    )
    
    # Use the new personality in a debate
    topic = "Should social media be regulated?"
    
    bot1, bot2 = factory.create_debate_pair(
        topic=topic,
        position1="Social media needs strict regulation",
        position2="Social media should remain largely unregulated",
        bot1_name="RegulatorBot",
        bot2_name="SarcasticFree",
        personality1="diplomatic",
        personality2="sarcastic",  # Our custom personality
        debate_style="casual"
    )
    
    example_logger.info(f"Created custom 'sarcastic' personality!")
    example_logger.info(f"Topic: {topic}")
    
    print(f"Created custom 'sarcastic' personality!")
    print(f"Topic: {topic}")
    
    # Just show the first exchange
    opening = factory.get_opening_prompt("casual")
    start_debate(bot1, bot2, initial_prompt=opening, max_rounds=1)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "demo":
            quick_demo()
        elif sys.argv[1] == "personalities":
            personality_showcase()
        elif sys.argv[1] == "custom":
            custom_personality_demo()
        else:
            example_logger.error("Invalid argument provided")
        print("Usage: python example.py [demo|personalities|custom]")
    else:
        example_logger.info("FightBot Example Script started")
        print("FightBot Example Script")
        print("Usage:")
        print("  python example.py demo         - Quick debate demo")
        print("  python example.py personalities - Show all personalities") 
        print("  python example.py custom       - Custom personality demo")