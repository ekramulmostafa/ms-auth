"""utils"""

import random
import string


from flask_mail import Message

from app.service import mail


def send_email(data: dict):
    """send email"""
    msg = Message(**data)
    mail.send(msg)
    return True


DEFAULT_CHAR_STRING = string.ascii_uppercase+string.ascii_lowercase + string.digits


def generate_random_string(chars=DEFAULT_CHAR_STRING, size=6):
    """generate random 6 character string"""
    return ''.join(random.choice(chars) for _ in range(size))
