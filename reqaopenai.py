import requests
from requests.exceptions import RequestException
import json
from copy import deepcopy
import logging


logger = logging.getLogger('OpenAIAPI')


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
            raise RequestException(f'status code {res.status_code}, payload content {res.text}')
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
        # logger.info(payload)

        res = self._make_request(url, method='POST', headers=headers, data=json.dumps(payload))

        return json.loads(res)['choices'][0]


if __name__ == '__main__':
    at = AutoText()
    while True:
        prompt = input()
        print(at.completion(prompt))
