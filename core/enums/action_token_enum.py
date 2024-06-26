from datetime import timedelta
from enum import Enum


class ActionEnum(Enum):
    ACTIVATE = ('activate', timedelta(minutes=30))
    RECOVERY = ('recovery', timedelta(minutes=30))

    def __init__(self, token_type, exp_time):
        self.token_type = token_type
        self.exp_time = exp_time
