import hashlib
import operator
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


def get_dict_from_list(data_list: list):
    data_dict: dict = {}
    for data in data_list:
        data_dict[data] = data_dict.get(data, 0) + 1
    return data_dict


def sort_dict(data: dict):
    sorted_dict = sorted(
        data.items(),
        key=operator.itemgetter(1),
        reverse=True
    )
    return sorted_dict
