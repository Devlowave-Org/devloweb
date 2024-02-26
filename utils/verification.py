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


def store_code(ja_id, code):
    devlobdd = bdd.DevloBDD()
    devlobdd.store_code(ja_id, code)
    devlobdd.quit_bdd()


if __name__ == "__main__":
    print(create_verification_code())