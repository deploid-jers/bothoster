from pwdlib import PasswordHash
import random

hash_to_check = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return hash_to_check.hash(password)

random_int_for_false_password = random.randint(100000, 1000000)
DUMMY_HASH = hash_password(f"false_{random_int_for_false_password}_hashed_password")

def verify_password(password: str, hashed_password: str) -> bool:
    return hash_to_check.verify(password, hashed_password)

