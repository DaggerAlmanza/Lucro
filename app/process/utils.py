import hashlib
import random


def hash_md5_util(password: str) -> str:
    """
    Hashcheamos la contraseña con md5

    Args:
        password (str): clave plana

    Returns:
        str: clave en md5
    """
    hashed_password = hashlib.md5(password.encode())
    password = hashed_password.hexdigest()
    return password


def generate_code() -> str:
    return str(random.getrandbits(128))
