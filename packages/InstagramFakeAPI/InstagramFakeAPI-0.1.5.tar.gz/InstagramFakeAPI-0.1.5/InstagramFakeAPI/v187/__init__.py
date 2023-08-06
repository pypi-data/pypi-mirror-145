import logging

from mixin.login import LoginAction
from InstagramFakeAPI.v187 import InstagramCustom


class Client(
    InstagramCustom,
    LoginAction
):
    logger = logging.getLogger("src")

    def __init__(self, logger):
        super(Client, self).__init__(logger)
