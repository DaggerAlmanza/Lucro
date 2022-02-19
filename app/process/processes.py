from .exceptions import UserProcessError
from .helpers import SessionManager
from .querysets import Queryset
from .utils import hash_md5_util
# , create_path_util


session_manager = SessionManager()


def create_user_process(data: dict):
    if not session_manager.get_login_status():
        data["password"] = hash_md5_util(data["password"])
        response = Queryset.create_user(data)
        return response
    raise UserProcessError(
        "One user is already logged",
        409
    )


def user_login_process(data: dict):
    if not session_manager.get_login_status():
        data["password"] = hash_md5_util(data["password"])
        response = Queryset.login_user(data)
        user_id = response.get("data").get("user_id")
        if user_id:
            session_manager.login(user_id)
            return response
        raise UserProcessError(
            "This user doesn't exist",
            404
        )
    raise UserProcessError(
        "The user is already logged",
        409
    )


def user_logout_process():
    if session_manager.get_login_status():
        session_manager.logout()
        return {
            "message": "Logout successfully"
        }
    raise UserProcessError(
        "The user is not login",
        409
    )
