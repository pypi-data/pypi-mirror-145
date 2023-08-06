import abc

from wiz_message.message import Message


class MessageGenerator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def to_message(self, message: Message):
        pass


class BotClient(metaclass=abc.ABCMeta):
    def __init__(self, webhook, secret_key):
        self._webhook = webhook
        self._secret_key = secret_key

    @property
    def webhook(self):
        return self._webhook

    @property
    def secret_key(self):
        return self._secret_key

    @classmethod
    @abc.abstractmethod
    def filter(cls, webhook: str):
        pass

    @abc.abstractmethod
    def send_message(self, message: Message):
        pass

    @abc.abstractmethod
    def convert_message(self, message: Message):
        pass


class BotClientHolder(object):
    def __init__(self, abs_client):
        self._clients = []
        self._abs_clients = abs_client

    @property
    def clients(self):
        return self._clients

    def gen_client(self, webhook: str, secret_key: str):
        for item in self._abs_clients:
            if item.filter(webhook):
                self._clients.append(item(webhook, secret_key))
                break

    def send_message(self, message: Message):
        for client in self._clients:
            client.send_message(message)
