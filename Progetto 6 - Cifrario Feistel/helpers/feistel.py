from helpers.key_gen import *
from helpers.utils import *


def encrypt(out_lck, file, chunk_len, key, rounds):
    output(out_lck, "Starting...")

    keys = gen_keys(key)

    