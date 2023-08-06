import logging

from InstagramFakeAPI.v159.mixin import LoginAction
from InstagramFakeAPI.v159.mixin.action import InstagramCustom


class Client(
    InstagramCustom,
    LoginAction
):
    logger = logging.getLogger("src")

    def __init__(self):
        super(Client, self).__init__()
