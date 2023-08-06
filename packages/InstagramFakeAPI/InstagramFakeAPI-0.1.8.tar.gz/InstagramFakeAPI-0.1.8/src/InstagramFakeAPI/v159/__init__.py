import logging

from .mixin.action import InstagramCustom


class Client(InstagramCustom):
    logger = logging.getLogger("Instagrm")

    def __init__(self):
        super(Client, self).__init__()
