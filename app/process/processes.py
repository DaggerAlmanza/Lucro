from app.process.webservices import process_images_services
from .exceptions import UserProcessError
from .helpers import SessionManager
from .querysets import Queryset
from .utils import hash_md5_util


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


def image_quantity_user_process():
    if session_manager.get_login_status():
        user_id: str = session_manager.get_user_id()
        count_images: int = Queryset.count_images_for_date(user_id)
        return {
            "message": f"You have {count_images} images uploaded in this day",
            "data": {
                "retries_qty": 5 - count_images
            }
        }
    raise UserProcessError(
        "The user is not login",
        401
    )


def upload_file_process(file: object, product_name: str):
    if session_manager.get_login_status():
        score_response: float = process_images_services(file)
        score: int = int(score_response*100)
        if score < 50:
            return {
                "message": "You won zero point,"
                           "your score must be at least 0.5",
                "data": {
                    "score": round(score_response, 2)
                }
            }

        is_checked: bool = False
        if score >= 80:
            is_checked = True
        user_id: str = session_manager.get_user_id()
        count_images: int = Queryset.count_images_for_date(user_id)

        if count_images < 5:
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
            "Exceeded the limit to upload images",
            400
        )
    raise UserProcessError(
        "The user is not login",
        401
    )


def show_registered_users_process():
    return Queryset.show_user()


def show_codes_process():
    return Queryset.show_codes()


def claim_codes_process(quantity):
    if session_manager.get_login_status():
        user_id: str = session_manager.get_user_id()
        response = Queryset.claim_codes(user_id, quantity)
        codes: list = response.get("codes")
        if codes:
            save_codes(user_id, codes)
            return {
                    "message": f"You have claimed, {quantity} code(s)",
                    "data": {
                        "codes": response["codes"]
                    }
                }
        return response

    raise UserProcessError(
        "The user is not login",
        401
    )


def save_codes(user_id: str, codes: list):
    for code in codes:
        is_saved = Queryset.save_code(
            user_id=user_id,
            code=code
        )
        if is_saved:
            Queryset.update_user_score(
                user_id,
                -1000
            )


def redeem_codes_process(code: str):
    return Queryset.redeem_code(code)


def show_user_score_process():
    if session_manager.get_login_status():
        user_id: str = session_manager.get_user_id()
        return Queryset.show_user_score(user_id)
    raise UserProcessError(
        "The user is not login",
        401
    )


def show_no_validate_image_process():
    return Queryset.show_no_validate_image()


def validate_image_process(identifier: str, is_validated: bool):
    return Queryset.validate_image(identifier, is_validated)


def show_most_registered_products_process():
    return Queryset.get_most_used_product()
