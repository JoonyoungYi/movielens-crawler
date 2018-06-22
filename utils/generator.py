import random
import string
from datetime import datetime
from datetime import timedelta


def generate_key(N=64):
    letters = string.ascii_letters + string.digits
    return ''.join((random.SystemRandom().choice(letters) for _ in range(N)))


def generate_10_key():
    return generate_key(N=10)


def generate_16_key():
    return generate_key(N=16)


def generate_50_key():
    return generate_key(N=50)


def generate_128_key():
    return generate_key(N=128)
