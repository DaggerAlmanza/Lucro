import logging
from fastapi import APIRouter, UploadFile
from fastapi.params import Form
from fastapi.responses import JSONResponse

from app.process.exceptions import UserProcessError
from app.process.handlers import (
    create_user_handler,
    delete_user_handler,
    edit_user_handler,
    show_codes_handler,
    show_most_registered_products_handler,
    show_no_validate_image_handler,
    show_registered_users_handler,
    show_user_score_handler,
    upload_file_handler,
    user_closed_session_handler,
    user_login_handler
)
from app.process.serializers import (
    ResponseSerializer,
    UserLoginSerializer,
    UserSerializer
)


router = APIRouter()
logger = logging.getLogger("router")


@router.post("/login", tags=["session"], response_model=ResponseSerializer)
async def login_user(user: UserLoginSerializer) -> dict:
    try:
        response = user_login_handler(user.dict())
        return JSONResponse(content=response, status_code=200)
    except UserProcessError as ue:
        logger.error(ue)
        response = {
            "error": ue.args[0]
        }
        return JSONResponse(
            content=response,
            status_code=ue.args[1]
        )
    except Exception as e:
        logger.error(e)
        response = {"error": str(e)}
        return JSONResponse(content=response, status_code=500)


@router.post("/logout", tags=["session"], response_model=ResponseSerializer)
async def close_session() -> dict:
    try:
        response = user_closed_session_handler()
        return JSONResponse(content=response, status_code=200)
    except UserProcessError as ue:
        logger.error(ue)
        response = {
            "error": ue.args[0]
        }
        return JSONResponse(
            content=response,
            status_code=ue.args[1]
        )
    except Exception as e:
        logger.error(e)
        response = {"error": str(e)}
        return JSONResponse(content=response, status_code=500)


@router.post("/create-user", tags=["user"], response_model=ResponseSerializer)
async def create_user(user: UserSerializer) -> dict:
    try:
        response = create_user_handler(user.dict())
        return JSONResponse(content=response, status_code=200)
    except UserProcessError as ue:
        logger.error(ue)
        response = {
            "error": ue.args[0]
        }
        return JSONResponse(
            content=response,
            status_code=ue.args[1]
        )
    except Exception as e:
        logger.error(e)
        response = {"error": str(e)}
        return JSONResponse(content=response, status_code=500)


@router.put("/edit-user", tags=["owner"], response_model=ResponseSerializer)
async def edit_user(
    user: UserSerializer,
    number_id: int
) -> dict:
    response = edit_user_handler(user, number_id)
    return JSONResponse(content=response, status_code=response.get("status"))


@router.delete(
    "/delete-user/{delete_id}",
    tags=["owner"],
    response_model=ResponseSerializer)
async def delete_user(delete_id: int) -> dict:
    return delete_user_handler(delete_id)


@router.post(
    "/verify-image",
    tags=["promo"],
    response_model=ResponseSerializer
)
async def upload_image(
    file: UploadFile,
    product_name: str = Form(...)
        ) -> dict:
    try:
        extension: str = file.filename.split(".")[1].lower()
        extensions: list = ["png", "jpg", "jpeg"]
        if extension not in extensions:
            raise UserProcessError(
                f"This is not an accepted image, type: {extension}",
                415
            )
        response = upload_file_handler(
            file,
            product_name)
        return JSONResponse(content=response, status_code=200)
    except UserProcessError as ue:
        logger.error(ue)
        response = {
            "error": ue.args[0]
        }
        return JSONResponse(
            content=response,
            status_code=ue.args[1]
        )
    except Exception as e:
        logger.error(e)
        response = {"error": str(e)}
        return JSONResponse(content=response, status_code=500)


@router.get(
    "/users",
    tags=["promo"],
    response_model=ResponseSerializer)
async def show_registered_users() -> dict:
    response = show_registered_users_handler()
    return JSONResponse(content=response, status_code=200)


@router.get(
    "/show-codes",
    tags=["promo"],
    response_model=ResponseSerializer)
async def show_codes() -> dict:
    response = show_codes_handler()
    return JSONResponse(content=response, status_code=200)


@router.get(
    "/show-products",
    tags=["promo"],
    response_model=ResponseSerializer)
async def show_most_registered_products() -> dict:
    response = show_most_registered_products_handler()
    return JSONResponse(content=response, status_code=200)


@router.get(
    "/show-user-score",
    tags=["promo"],
    response_model=ResponseSerializer)
async def show_user_score() -> dict:
    response = show_user_score_handler()
    return JSONResponse(content=response, status_code=200)


@router.get(
    "/show-no-validate-image",
    tags=["user"],
    response_model=ResponseSerializer)
async def show_no_validate_image() -> dict:
    response = show_no_validate_image_handler()
    return JSONResponse(content=response, status_code=200)
