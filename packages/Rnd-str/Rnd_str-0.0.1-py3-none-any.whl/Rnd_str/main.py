import random as rn
import string

def random_str(length=5):
    chrs = string.ascii_letters + string.digits + "!@#$%^&*_+~"
    result = "".join(rn.choice(chrs) for _ in range(length))
    return result
    # print("Error! You must give a function a numeric value.")