import os
from LinuxServerStatsTelegramBot.sender.Sender import Sender


class DI:
    sender: Sender

    @classmethod
    def set_sender(cls, sender: Sender):
        cls.sender = sender

    @classmethod
    def get_sender(cls) -> Sender:
        return cls.sender

    @staticmethod
    def get_server_name() -> str:
        server_alias = os.getenv("LSSTB_SERVER_ALIAS", "Unamed Server")
        return server_alias

    @staticmethod
    def project_root() -> str:
        return os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def get_tg_bot_token():
        token = os.getenv("LSSTB_BOT")
        return token

    @staticmethod
    def get_tg_chat_id():
        chat_id = os.getenv("LSSTB_CHAT")
        return chat_id
