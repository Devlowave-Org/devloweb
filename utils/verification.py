import bdd
import random
import string


def create_verification_code() -> str:
    length = 4
    code = ""
    for i in range(length):
        code += random.choice(string.ascii_letters)
        code += str(random.randint(0, 9))
    return code
