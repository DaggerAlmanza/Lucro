import logging
from fastapi import APIRouter
from fastapi.params import File, Form
from fastapi.responses import JSONResponse

from app.process.exceptions import UserProcessError
from app.process.handlers import create_user_handler, user_login_handler,\
    user_closed_session_handler, edit_user_handler, delete_user_handler,\
    show_user_handler, upload_file_handler
from app.process.serializers import UserSerializer, UserLoginSerializer,\
    ResponseSerializer


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


@router.put("/edit-user", tags=["user"], response_model=ResponseSerializer)
async def edit_user(
    user: UserSerializer,
    number_id: int
) -> dict:
    response = edit_user_handler(user, number_id)
    return JSONResponse(content=response, status_code=response.get("status"))


@router.delete(
    "/delete-user/{delete_id}",
    tags=["user"],
    response_model=ResponseSerializer)
async def delete_user(delete_id: int) -> dict:
    return delete_user_handler(delete_id)


@router.get("/show-user", tags=["user"], response_model=ResponseSerializer)
async def show_user() -> dict:
    response = show_user_handler()
    return JSONResponse(content=response, status_code=response.get("status"))


@router.post("/create-upload", tags=["upload"], response_model=ResponseSerializer)
async def create_upload_file(
    photo_file: bytes = File(...),
    date_id_register: str = Form(...)
        ) -> dict:
    response = upload_file_handler(
        photo_file,
        date_id_register)
    return JSONResponse(content=response, status_code=response.get("status"))
