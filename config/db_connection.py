import os
from mongoengine import connect


def connect_db() -> None:
    """

    :return: connect mongodb
    """
    connect(
        host=os.getenv("MONGO_URI")
    )