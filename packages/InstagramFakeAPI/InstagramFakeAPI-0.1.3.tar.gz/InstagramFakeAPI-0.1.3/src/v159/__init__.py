import logging

from src.v159.mixin.login import LoginAction
from src.v159.mixin.action import InstagramCustom


class Client(
    InstagramCustom,
    LoginAction
):
    logger = logging.getLogger("src")

    def __init__(self):
        super(Client, self).__init__()
