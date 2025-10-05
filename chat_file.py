import logging
import tempfile
import os
from datetime import datetime
from threading import Thread
from time import sleep

from reqaopenai import AutoText

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class ChatBot:
    def __init__(self, filename='./chat1.txt', response='./chat2.txt', output='./output.txt'):
        self.at = AutoText()
        self.file = open(filename, 'r')
        self.output = output
        self.response = response
        
        # Setup logging for this file-based bot
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_dir = tempfile.mkdtemp(prefix="chatfile_bot_")
        log_file = os.path.join(log_dir, f"file_bot_{timestamp}.log")
        
        self.logger = logging.getLogger(f"FileChatBot_{id(self)}")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        
        self.logger.info(f"File-based ChatBot initialized")
        self.logger.info(f"Input file: {filename}")
        self.logger.info(f"Response file: {response}")
        self.logger.info(f"Output file: {output}")
        self.logger.info(f"Log file: {log_file}")

    def __del__(self):
        self.file.close()

    def read(self):
        self.logger.info("Starting file monitoring loop")
        while True:
            try:
                content = self.file.read()
                if len(content) > 1:
                    self.logger.info(f"Read content from file: {content[:100]}..." if len(content) > 100 else f"Read content: {content}")
                    
                    res = self.at.chat_single(content)
                    self.logger.info(f"Generated response: {res[:100]}..." if len(res) > 100 else f"Generated response: {res}")
                    
                    # Write to output file
                    with open(self.output, 'a') as f:
                        f.write(res)
                        f.flush()
                    self.logger.debug(f"Response written to output file: {self.output}")
                    
                    # Write to response file
                    with open(self.response, 'a') as f:
                        f.write(res)
                        f.flush()
                    self.logger.debug(f"Response written to response file: {self.response}")
                    
            except EOFError:
                self.logger.debug("EOFError encountered, continuing...")
                sleep(1)
            except Exception as e:
                self.logger.error(f"Error in read loop: {e}")
                
            sleep(5)


if __name__ == "__main__":
    main_logger = logging.getLogger("FileChatMain")
    
    main_logger.info("Starting file-based chat system")
    
    try:
        cb1 = ChatBot(filename='./chat1.txt', response='./chat2.txt')
        main_logger.info("Created first chatbot")
        
        t = Thread(target=cb1.read)
        t.start()
        main_logger.info("Started first chatbot thread")
        
        cb2 = ChatBot(filename='./chat2.txt', response='./chat1.txt')
        main_logger.info("Created second chatbot")
        
        main_logger.info("Starting second chatbot (main thread)")
        cb2.read()
        
    except KeyboardInterrupt:
        main_logger.info("File chat system interrupted by user")
    except Exception as e:
        main_logger.error(f"Error in file chat system: {e}")
