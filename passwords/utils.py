import random

chars = "abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!?@#$%_"
size = 20


def password_generator():
    """A function that generator a random password"""
    password = "".join(random.sample(chars, size))
    return password
