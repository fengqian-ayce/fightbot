import logging
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from time import sleep

from reqaopenai import AutoText

logging.basicConfig(level=logging.INFO)


class ChatBot:
    DEFAULT_CONFIG = [
        {"role": "system", "content": "try to give short answer"}
    ]

    def __init__(self, name: str, output='response.txt'):
        self.at = AutoText()
        self.name = name
        self.output = output
        self.conversation = []

        self.logger = logging.getLogger(f"ChatBot_{name}")
        self.logger.setLevel(logging.INFO)

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


def create_debate_bots(topic: str, position1: str, position2: str, bot1_name: str = "Bot1", bot2_name: str = "Bot2"):
    """
    Create two debate bots with opposing viewpoints on a given topic.
    
    Args:
        topic (str): The debate topic
        position1 (str): The position that bot1 will support
        position2 (str): The position that bot2 will support
        bot1_name (str): Name for the first bot
        bot2_name (str): Name for the second bot
    
    Returns:
        tuple: (bot1, bot2) configured ChatBot instances
    """
    cb1_content = [
        {
            "role": "system",
            "content": f"Please act like you are attending a public debate. Your strength is making emotional and passionate arguments. The topic is: {topic}. You support {position1}. Be persuasive and use compelling examples."
        },
        {
            "role": "user",
            "content": f"{position2} is better. Try to change my mind about {topic}."
        }
    ]

    cb2_content = [
        {
            "role": "system",
            "content": f"Act like you are attending a public debate. Use a balanced strategy between attacking your opponent's points and explaining your own position. Keep an eye on logical fallacies in your opponent's answers. Give well-reasoned, analytical responses. The topic is: {topic}. You support {position2}."
        }
    ]

    cb1 = ChatBot(bot1_name)
    cb1.create_role(cb1_content)
    
    cb2 = ChatBot(bot2_name)
    cb2.create_role(cb2_content)
    
    return cb1, cb2


def start_debate(bot1, bot2, initial_prompt: str = "please present your opening argument", max_rounds: int = None):
    """
    Start a debate between two bots.
    
    Args:
        bot1: First ChatBot instance
        bot2: Second ChatBot instance
        initial_prompt (str): The initial prompt to start the debate
        max_rounds (int): Maximum number of debate rounds (None for unlimited)
    """
    print(f"\n=== DEBATE STARTED ===")
    print(f"Bot 1: {bot1.name}")
    print(f"Bot 2: {bot2.name}")
    print("=" * 50)
    
    res2 = bot2.add_response(initial_prompt)
    print(f"\n{bot2.name}: {res2}")
    print("-" * 50)
    
    round_count = 1
    while max_rounds is None or round_count <= max_rounds:
        try:
            res1 = bot1.add_response(res2)
            print(f"\n{bot1.name}: {res1}")
            print("-" * 50)
            
            sleep(1)
            
            res2 = bot2.add_response(res1)
            print(f"\n{bot2.name}: {res2}")
            print("-" * 50)
            
            round_count += 1
            
        except KeyboardInterrupt:
            print("\n\nDebate interrupted by user.")
            break
        except Exception as e:
            print(f"\nError during debate: {e}")
            break


def get_user_input():
    """Get debate topic and positions from user input."""
    print("Welcome to FightBot Debate System!")
    print("=" * 40)
    
    topic = input("\nEnter the debate topic: ").strip()
    while not topic:
        topic = input("Please enter a valid topic: ").strip()
    
    position1 = input(f"\nEnter the first position on '{topic}': ").strip()
    while not position1:
        position1 = input("Please enter a valid first position: ").strip()
    
    position2 = input(f"\nEnter the opposing position on '{topic}': ").strip()
    while not position2:
        position2 = input("Please enter a valid opposing position: ").strip()
    
    bot1_name = input(f"\nName for bot supporting '{position1}' (default: Pro): ").strip()
    if not bot1_name:
        bot1_name = "Pro"
    
    bot2_name = input(f"Name for bot supporting '{position2}' (default: Con): ").strip()
    if not bot2_name:
        bot2_name = "Con"
    
    try:
        max_rounds = input("\nMaximum number of debate rounds (press Enter for unlimited): ").strip()
        max_rounds = int(max_rounds) if max_rounds else None
    except ValueError:
        max_rounds = None
        print("Invalid number entered, using unlimited rounds.")
    
    return topic, position1, position2, bot1_name, bot2_name, max_rounds


if __name__ == "__main__":
    try:
        # Get user input for debate configuration
        topic, pos1, pos2, name1, name2, max_rounds = get_user_input()
        
        print(f"\nSetting up debate...")
        print(f"Topic: {topic}")
        print(f"{name1} supports: {pos1}")
        print(f"{name2} supports: {pos2}")
        
        # Create debate bots
        bot1, bot2 = create_debate_bots(topic, pos1, pos2, name1, name2)
        
        # Start the debate
        start_debate(bot1, bot2, max_rounds=max_rounds)
        
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
