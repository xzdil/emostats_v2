from .base import *

class Message(BaseValidateModel):
    status: str
    message: str
