import logging

from src.v187.mixin.login import LoginAction
from src.v187.mixin.action import InstagramCustom


class Client(
    InstagramCustom,
    LoginAction
):
    logger = logging.getLogger("src")

    def __init__(self, logger):
        super(Client, self).__init__(logger)
