from app.process.processes import create_user_process, user_login_process,\
    user_logout_process


def user_login_handler(user: dict) -> dict:
    return user_login_process(user)


def user_closed_session_handler() -> dict:
    return user_logout_process()


def create_user_handler(user: dict) -> dict:
    return create_user_process(user)


def edit_user_handler(user, number_id) -> dict:
    pass


def delete_user_handler(delete_id) -> dict:
    pass


def show_user_handler() -> dict:
    pass


def upload_file_handler(
    photo_file,
    date_id_register
) -> dict:
    pass
