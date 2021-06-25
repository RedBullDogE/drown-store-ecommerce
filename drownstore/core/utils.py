import random
import string


def generate_random_code(length):
    """
    Generating random string with specified length, consisting of
    ascii_letters and digits.
    """
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
