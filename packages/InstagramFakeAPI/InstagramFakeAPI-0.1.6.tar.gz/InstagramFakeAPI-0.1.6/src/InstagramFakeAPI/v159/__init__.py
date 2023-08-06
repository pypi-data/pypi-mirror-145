import logging

from src.InstagramFakeAPI.v159 import LoginAction
from src.InstagramFakeAPI.v159.mixin.action import InstagramCustom


class Client(
    InstagramCustom,
    LoginAction
):
    logger = logging.getLogger("src")

    def __init__(self):
        super(Client, self).__init__()
