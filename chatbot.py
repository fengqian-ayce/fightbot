import logging
import tempfile
import os
from datetime import datetime
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from time import sleep
from typing import Tuple

from reqaopenai import AutoText
from topic_selector import TopicSelector, TopicManager, manage_topics

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)



class ChatBot:
    DEFAULT_CONFIG = [
        {"role": "system", "content": "try to give short answer"}
    ]

    def __init__(self, name: str, output='response.txt', log_file=None):
        self.at = AutoText()
        self.name = name
        self.output = output
        self.conversation = []
        self.log_file = log_file

        # Setup logger for this bot
        self.logger = logging.getLogger(f"ChatBot_{name}")
        self.logger.setLevel(logging.INFO)
        
        # Add file handler if log_file is provided
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            self.logger.addHandler(file_handler)

    def create_role(self, config: list):
        if config is None:
            self.conversation.extend(self.DEFAULT_CONFIG)
        else:
            self.conversation.extend(config)

    def respond(self, chat):
        res = self.at.chat(chat, self.conversation)
        return res['message']
    
    def add_response(self, chat, delay=1):
        res = self.respond(chat)
        self.logger.debug("responding...")
        self.logger.info(res['content'])
        self.conversation.append(res)
        self.logger.info(self.conversation)
        sleep(delay)
        return res['content']

    def communicate(self, pipe: Connection, delay=1):
        while True:
            question = pipe.recv()
            self.logger.info('request received')
            if len(question) > 1:
                self.logger.info("request sent")
                res = self.at.chat(question, self.conversation)
                self.conversation.append(res['message'])
                response = res['message']['content']
                self.logger.info(response)
                with open(self.output, 'a') as f:
                    f.write(response)
                    f.flush()
                self.logger.info('response sent to opponent')
                pipe.send(response)
            sleep(delay)





def start_debate(bot1, bot2, initial_prompt: str = "please present your opening argument", max_rounds: int = None):
    """
    Start a debate between two bots.
    
    Args:
        bot1: First ChatBot instance
        bot2: Second ChatBot instance
        initial_prompt (str): The initial prompt to start the debate
        max_rounds (int): Maximum number of debate rounds (None for unlimited)
    """
    # Create temporary log file for this debate session
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = tempfile.mkdtemp(prefix="fightbot_debate_")
    debate_log = os.path.join(log_dir, f"debate_{timestamp}.log")
    
    # Setup debate logger
    debate_logger = logging.getLogger("DebateSession")
    debate_handler = logging.FileHandler(debate_log)
    debate_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    debate_logger.addHandler(debate_handler)
    
    debate_logger.info("=== DEBATE STARTED ===")
    debate_logger.info(f"Bot 1: {bot1.name}")
    debate_logger.info(f"Bot 2: {bot2.name}")
    debate_logger.info(f"Log file: {debate_log}")
    debate_logger.info(f"Initial prompt: {initial_prompt}")
    debate_logger.info("=" * 50)
    
    # Also print to console for immediate feedback
    console_logger = logging.getLogger("Console")
    console_logger.info(f"\n=== DEBATE STARTED ===")
    console_logger.info(f"Bot 1: {bot1.name}")
    console_logger.info(f"Bot 2: {bot2.name}")
    console_logger.info(f"Debate log: {debate_log}")
    console_logger.info("=" * 50)
    
    res2 = bot2.add_response(initial_prompt)
    debate_logger.info(f"ROUND 0 - {bot2.name}: {res2}")
    console_logger.info(f"\n{bot2.name}: {res2}")
    console_logger.info("-" * 50)
    
    round_count = 1
    while max_rounds is None or round_count <= max_rounds:
        try:
            res1 = bot1.add_response(res2)
            debate_logger.info(f"ROUND {round_count} - {bot1.name}: {res1}")
            console_logger.info(f"\n{bot1.name}: {res1}")
            console_logger.info("-" * 50)
            
            sleep(1)
            
            res2 = bot2.add_response(res1)
            debate_logger.info(f"ROUND {round_count} - {bot2.name}: {res2}")
            console_logger.info(f"\n{bot2.name}: {res2}")
            console_logger.info("-" * 50)
            
            round_count += 1
            
        except KeyboardInterrupt:
            debate_logger.info("Debate interrupted by user")
            console_logger.info("\n\nDebate interrupted by user.")
            break
        except Exception as e:
            debate_logger.error(f"Error during debate: {e}")
            console_logger.error(f"\nError during debate: {e}")
            break
    
    # Close debate session
    debate_logger.info("=== DEBATE ENDED ===")
    debate_logger.info(f"Total rounds completed: {round_count - 1}")
    console_logger.info(f"\n=== DEBATE ENDED ===")
    console_logger.info(f"Total rounds: {round_count - 1}")
    console_logger.info(f"Full debate log saved to: {debate_log}")
    
    # Remove handler to avoid memory leaks
    debate_logger.removeHandler(debate_handler)
    debate_handler.close()
    
    return debate_log


def get_latest_debate_log():
    """Get the path to the most recent debate log file."""
    import glob
    
    temp_dir = tempfile.gettempdir()
    debate_dirs = glob.glob(os.path.join(temp_dir, "fightbot_debate_*"))
    
    if not debate_dirs:
        return None
    
    # Get most recent directory
    latest_dir = max(debate_dirs, key=os.path.getmtime)
    
    # Find log files in that directory
    log_files = glob.glob(os.path.join(latest_dir, "*.log"))
    
    if log_files:
        return max(log_files, key=os.path.getmtime)
    
    return None


def get_user_input():
    """Get debate topic and positions from user input."""
    from bot_factory import BotFactory
    
    logger = logging.getLogger("UserInput")
    factory = BotFactory()
    topic_selector = TopicSelector()
    
    logger.info("Welcome to FightBot Debate System!")
    logger.info("=" * 40)
    print("Welcome to FightBot Debate System!")
    print("=" * 40)
    
    # Get topic selection using the modular selector
    topic, position1, position2, mode = topic_selector.get_topic_selection()
    
    logger.info(f"Selected input mode: {mode}")
    logger.info(f"Selected topic: {topic}")
    logger.info(f"Position 1: {position1}")
    logger.info(f"Position 2: {position2}")
    
    bot1_name = input(f"\nName for bot supporting '{position1}' (default: Pro): ").strip()
    if not bot1_name:
        bot1_name = "Pro"
    
    bot2_name = input(f"Name for bot supporting '{position2}' (default: Con): ").strip()
    if not bot2_name:
        bot2_name = "Con"
    
    # Show available personalities
    logger.info("Available Bot Personalities:")
    print("\nAvailable Bot Personalities:")
    personalities = factory.list_personalities()
    for i, (pid, info) in enumerate(personalities.items(), 1):
        personality_info = f"  {i}. {pid}: {info['name']} - {info['description']}"
        logger.info(personality_info)
        print(personality_info)
    
    # Get personality choices
    personality_ids = list(personalities.keys())
    
    try:
        choice1 = input(f"\nChoose personality for {bot1_name} (1-{len(personality_ids)} or press Enter for 'emotional'): ").strip()
        if choice1 and choice1.isdigit():
            idx = int(choice1) - 1
            if 0 <= idx < len(personality_ids):
                personality1 = personality_ids[idx]
            else:
                personality1 = 'emotional'
        else:
            personality1 = 'emotional'
    except ValueError:
        personality1 = 'emotional'
    
    try:
        choice2 = input(f"Choose personality for {bot2_name} (1-{len(personality_ids)} or press Enter for 'logical'): ").strip()
        if choice2 and choice2.isdigit():
            idx = int(choice2) - 1
            if 0 <= idx < len(personality_ids):
                personality2 = personality_ids[idx]
            else:
                personality2 = 'logical'
        else:
            personality2 = 'logical'
    except ValueError:
        personality2 = 'logical'
    
    # Show available debate styles
    logger.info("Available Debate Styles:")
    print("\nAvailable Debate Styles:")
    styles = factory.list_debate_styles()
    style_ids = list(styles.keys())
    for i, (sid, info) in enumerate(styles.items(), 1):
        style_info = f"  {i}. {sid}: {info['opening_prompt']}"
        logger.info(style_info)
        print(style_info)
    
    try:
        style_choice = input(f"\nChoose debate style (1-{len(style_ids)} or press Enter for 'casual'): ").strip()
        if style_choice and style_choice.isdigit():
            idx = int(style_choice) - 1
            if 0 <= idx < len(style_ids):
                debate_style = style_ids[idx]
            else:
                debate_style = 'casual'
        else:
            debate_style = 'casual'
    except ValueError:
        debate_style = 'casual'
    
    try:
        max_rounds = input("\nMaximum number of debate rounds (press Enter for unlimited): ").strip()
        max_rounds = int(max_rounds) if max_rounds else None
    except ValueError:
        max_rounds = None
        print("Invalid number entered, using unlimited rounds.")
    
    return topic, position1, position2, bot1_name, bot2_name, max_rounds, personality1, personality2, debate_style, mode


if __name__ == "__main__":
    try:
        from bot_factory import BotFactory
        
        # Get user input for debate configuration
        result = get_user_input()
        topic, pos1, pos2, name1, name2, max_rounds, personality1, personality2, debate_style = result[:9]
        
        # Extract mode for later use
        mode = result[9] if len(result) > 9 else 'interactive'
        topic_selector = TopicSelector()
        
        main_logger = logging.getLogger("Main")
        
        main_logger.info(f"Setting up debate...")
        main_logger.info(f"Topic: {topic}")
        main_logger.info(f"{name1} ({personality1}) supports: {pos1}")
        main_logger.info(f"{name2} ({personality2}) supports: {pos2}")
        main_logger.info(f"Debate style: {debate_style}")
        main_logger.info(f"Topic source: {'predefined' if topic in [t['topic'] for t in TopicManager().topics.values()] else 'custom'}")
        
        # Ask if user wants to manage topics before starting debate
        if mode == 'file' and not topic_selector.topic_manager.topics:
            manage_choice = input("\nNo topics found in file. Would you like to add some topics first? (y/N): ").strip().lower()
            if manage_choice == 'y':
                manage_topics()
                # Reload topics after management
                topic_selector.topic_manager.load_topics()
        
        print(f"\nSetting up debate...")
        print(f"Topic: {topic}")
        print(f"{name1} ({personality1}) supports: {pos1}")
        print(f"{name2} ({personality2}) supports: {pos2}")
        print(f"Debate style: {debate_style}")
        
        # Create debate bots using factory
        factory = BotFactory()
        bot1, bot2 = factory.create_debate_pair(
            topic, pos1, pos2, name1, name2, 
            personality1, personality2, debate_style
        )
        
        # Get appropriate opening prompt for the debate style
        opening_prompt = factory.get_opening_prompt(debate_style)
        
        # Start the debate
        debate_log_file = start_debate(bot1, bot2, initial_prompt=opening_prompt, max_rounds=max_rounds)
        main_logger.info(f"Debate completed. Log saved to: {debate_log_file}")
        
        # Offer topic management after debate
        if mode == 'interactive':
            topic_selector.offer_topic_saving(topic, pos1, pos2)
        
    except KeyboardInterrupt:
        main_logger.info("Program terminated by user")
        print("\nProgram terminated by user.")
        print("\nTip: You can manage topics by running the topic manager separately.")
    except Exception as e:
        main_logger.error(f"An error occurred: {e}")
        print(f"\nAn error occurred: {e}")
        print("\nNote: If you're having trouble with topics, you can manage them using the topic manager.")


# Standalone topic management function that can be called separately
def run_topic_manager():
    """Run the topic manager as a standalone utility."""
    try:
        manage_topics()
    except KeyboardInterrupt:
        print("\nTopic manager closed.")
    except Exception as e:
        print(f"\nError in topic manager: {e}")
