from app.process.processes import (
    create_user_process,
    claim_codes_process,
    image_quantity_user_process,
    redeem_codes_process,
    show_most_registered_products_process,
    show_no_validate_image_process,
    show_registered_users_process,
    show_codes_process,
    show_user_score_process,
    upload_file_process,
    user_login_process,
    user_logout_process,
    validate_image_process
)


def user_login_handler(user: dict) -> dict:
    return user_login_process(user)


def user_closed_session_handler() -> dict:
    return user_logout_process()


def create_user_handler(user: dict) -> dict:
    return create_user_process(user)


def edit_user_handler() -> dict:
    pass


def delete_user_handler() -> dict:
    pass


def upload_file_handler(
    file,
    product_name
) -> dict:
    return upload_file_process(file, product_name)


def show_registered_users_handler():
    return show_registered_users_process()


def show_codes_handler():
    return show_codes_process()


def show_most_registered_products_handler():
    return show_most_registered_products_process()


def show_user_score_handler():
    return show_user_score_process()


def show_no_validate_image_handler():
    return show_no_validate_image_process()


def claim_codes_handler(quantity: int):
    return claim_codes_process(quantity)


def redeem_codes_handler(code: str):
    return redeem_codes_process(code)


def validate_image_handler(identifier: str, is_validated: bool):
    return validate_image_process(identifier, is_validated)


def image_quantity_user_handler():
    return image_quantity_user_process()
