import logging

from .mixin.action import InstagramCustom


class Client(InstagramCustom):
    logger = logging.getLogger("src")

    def __init__(self, logger):
        super(Client, self).__init__(logger)
