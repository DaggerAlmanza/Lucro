from app.process.webservices import process_images_services
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


def upload_file_process(file: object, product_name: str):
    if session_manager.get_login_status():
        score_response: float = process_images_services(file)
        score: int = int(score_response*100)
        if score < 50:
            return {"message": "The image is bad, you won zero point"}

        is_checked: bool = False
        if score >= 80:
            is_checked = True
        user_id: str = session_manager.get_user_id()
        Queryset.register_image(
            user_id,
            product_name,
            score,
            is_checked
        )
        Queryset.update_user_score(
            user_id,
            score
        )
        return {

            "data": {
                "score": score,
                "validate": is_checked
            },
            "message": "Image registered successfully"
            }
    raise UserProcessError(
        "The user is not login",
        401
    )
