from reqaopenai import AutoText
from time import sleep
from threading import Thread


class ChatBot:
    def __init__(self, filename='./chat1.txt', response='./chat2.txt', output='./output.txt'):
        self.at = AutoText()
        self.file = open(filename, 'r')
        self.output = output
        self.response = response

    def __del__(self):
        self.file.close()

    def read(self):
        while True:
            try:
                content = self.file.read()
                if len(content) > 1:
                    res = self.at.chat_single(content)
                    with open(self.output, 'a') as f:
                        f.write(res)
                        f.flush()
                    with open(self.response, 'a') as f:
                        f.write(res)
                        f.flush()
            except EOFError:
                sleep(1)
            sleep(5)


if __name__ == "__main__":
    cb1 = ChatBot(filename='./chat1.txt', response='./chat2.txt')
    t = Thread(target=cb1.read)
    t.start()
    cb2 = ChatBot(filename='./chat2.txt', response='./chat1.txt')
    cb2.read()