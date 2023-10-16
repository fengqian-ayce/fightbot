import logging
from multiprocessing import Pipe, Process
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
        return res['message']['content']
    
    def add_response(self, chat, delay=1):
        res = self.respond(chat)
        self.logger.debug("responding...")
        self.logger.info(res)
        self.conversation.append(res)
        sleep(delay)
        return res

    def communicate(self, pipe: Pipe, delay=1):
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


if __name__ == "__main__":
    cb1_content = [
        {
            "role": "system",
            "content": "please act like you are attending public debating. Your strength is making the argument emotional. the topic is: which one is better, big government or small government. You support big government."},
        {
            "role": "user",
            "content": "small goverment is better, try to change my mind"}
    ]

    cb2_content = [{"role": "system",
                    "content": "Act like you are attending public debating. Use a balanced strategy between attacking your opponent's point and explaining your own point. Keep an eye on logical fallacies in your opponent's answer. Give GRE argument style response when suitable. the topic is: which one is better, big government or small government. You support small government."}]

    cb1 = ChatBot('BigGov')
    cb1.create_role(cb1_content)

    # main_conn, cb_conn = Pipe()
    # cb1_proc = Process(target=cb1.communicate, args=(cb_conn,), daemon=True)
    # cb1_proc.start()

    sleep(1)

    # main_conn.send('please change my view')

    cb2 = ChatBot('SmallGov')
    cb2.create_role(cb2_content)

    # cb2.communicate(main_conn)

    res2 = cb2.add_response('please change my view')
    while True:
        res1 = cb1.add_response(res2)
        sleep(1)
        res2 = cb2.add_response(res1)
