import uuid
from datetime import datetime


class GeneralHelpers:

    @staticmethod
    def get_datetime():
        """
        Method for getting time
        :return:
        """
        time = datetime.now()
        return time

    @staticmethod
    def get_date_from():
        time = datetime.now().date()
        return time

    @staticmethod
    def get_date_to():
        """
        Method for getting time
        :return:
        """
        today = datetime.now()
        today_year = today.year
        today_month = today.month
        today_day = today.day

        time = datetime(today_year, today_month, today_day)

        timestamp = datetime.timestamp(time) + 86400
        time = datetime.fromtimestamp(timestamp)
        return time

    @staticmethod
    def get_iso_time():
        """
        Method for getting time
        :return:
        """
        time = datetime.now().isoformat()
        return time

    @staticmethod
    def get_uuid():
        """
        Method for generating uuid
        :return: uuid string
        """
        guid = uuid.uuid4()
        return str(guid)


class SessionManager:
    def __init__(self) -> None:
        self.__user_id: str = ""
        self.__is_logged: bool = False

    def get_login_status(self) -> bool:
        return self.__is_logged

    def get_user_id(self) -> str:
        return self.__user_id

    def login(self, user_id: str):
        self.__user_id = user_id
        self.__is_logged = True

    def logout(self):
        self.__is_logged = False
        self.__user_id = ""
