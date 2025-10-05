import json
import logging
from copy import deepcopy

import requests
from requests.exceptions import RequestException

# Setup logging for OpenAI API
logger = logging.getLogger('OpenAIAPI')
logger.setLevel(logging.INFO)


class AutoText:

    def __init__(self, text_source: str = 'openai', token=''):
        if token == '':
            with open('config.json', 'r') as f:
                config = json.load(f)
            token = config['openAI']['token']
        self.HEAD = {
            "Authorization": f"Bearer {token}"
        }
        if text_source == 'openai':
            self.base_url = "https://api.openai.com/"
        else:
            raise NotImplementedError

    def _make_request(self, url, method='GET', **kwargs):
        if method == 'GET':
            res = requests.get(url, headers=kwargs.get('headers', self.HEAD))
        elif method == "POST":
            res = requests.post(url, data=kwargs.get('data'), headers=kwargs.get('headers', self.HEAD))
        else:
            raise NotImplementedError(f'method {method} not supported yet')
        if res.status_code not in (200, 201):
            error_msg = f'HTTP {res.status_code}: {res.text}'
            logger.error(f"API request failed: {error_msg}")
            raise RequestException(error_msg)
        
        logger.debug(f"API request successful: {method} {url}")
        return res.text

    def list_models(self):
        url = self.base_url + 'v1/models'
        model_raw = json.loads(self._make_request(url, method='GET'))
        return model_raw['data']

    def retrieve_model(self, model):
        url = self.base_url + f'v1/models/{model}'
        return json.loads(self._make_request(url, method='GET'))

    def completion(self,
                   prompt="",
                   model="text-davinci-003",
                   temperature=0,
                   max_tokens=32
                   ):
        url = self.base_url + f'v1/completions'
        headers = deepcopy(self.HEAD)
        headers['Content-Type'] = "application/json"

        content = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        res = self._make_request(url, method='POST', headers=headers, data=json.dumps(content))
        texts = [i['text'].strip('\n') for i in json.loads(res)['choices']]
        return texts[0] if len(texts) == 1 else texts

    def chat_single(self, content, role="user"):
        url = self.base_url + f'v1/chat/completions'
        headers = deepcopy(self.HEAD)
        headers['Content-Type'] = "application/json"
        message = {
            "role": role,
            "content": content
        }
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": [message]
        }
        res = self._make_request(url, method='POST', headers=headers, data=json.dumps(payload))
        texts = [i['message']['content'].strip('\n') for i in json.loads(res)['choices']]

        return ''.join(texts)

    def chat(self, content, messages, role="user"):
        url = self.base_url + f'v1/chat/completions'
        headers = deepcopy(self.HEAD)
        headers['Content-Type'] = "application/json"
        message = {
            "role": role,
            "content": content
        }

        # messages.append(message)

        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages + [message]
        }
        logger.debug(f"Chat request payload: {len(payload['messages'])} messages")
        logger.debug(f"User message: {content[:100]}..." if len(content) > 100 else f"User message: {content}")

        res = self._make_request(url, method='POST', headers=headers, data=json.dumps(payload))
        logger.debug("Chat response received successfully")

        return json.loads(res)['choices'][0]


if __name__ == '__main__':
    # Setup logging for interactive mode
    logging.basicConfig(level=logging.INFO)
    test_logger = logging.getLogger("AutoTextTest")
    
    at = AutoText()
    test_logger.info("AutoText interactive mode started. Type 'quit' to exit.")
    
    while True:
        try:
            prompt = input("Enter prompt: ")
            if prompt.lower() in ['quit', 'exit']:
                test_logger.info("Exiting interactive mode")
                break
            
            response = at.completion(prompt)
            test_logger.info(f"Response generated for prompt: {prompt[:50]}...")
            print(response)
            
        except KeyboardInterrupt:
            test_logger.info("\nInterrupted by user")
            break
        except Exception as e:
            test_logger.error(f"Error: {e}")
            print(f"Error: {e}")
