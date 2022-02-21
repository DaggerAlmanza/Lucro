import logging
from fastapi import APIRouter, Header, UploadFile
from fastapi.params import Form
from fastapi.responses import JSONResponse

from app.process.constants import API_KEY
from app.process.exceptions import UserProcessError
from app.process.handlers import (
    create_user_handler,
    delete_user_handler,
    edit_user_handler,
    claim_codes_handler,
    image_quantity_user_handler,
    redeem_codes_handler,
    show_codes_handler,
    show_most_registered_products_handler,
    show_no_validate_image_handler,
    show_registered_users_handler,
    show_user_score_handler,
    upload_file_handler,
    user_closed_session_handler,
    user_login_handler,
    validate_image_handler
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
    """
    El usuario inicia sesión
    Args:
        user (UserLoginSerializer):
            email: str
            password: str

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
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
    """
    El usuario cierra sesión

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
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
    """
    Creación de un usuario

    Args:
        user (UserSerializer):
            fullname: str
            identification: int
            email: str
            password: str

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
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


@router.post(
    "/image-quantity-user",
    tags=["promo"],
    response_model=ResponseSerializer)
async def image_quantity_user() -> dict:
    """
    Oportunidades que le quedan al usuario para subir una foto en el día

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
    try:
        response = image_quantity_user_handler()
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


@router.post(
    "/verify-image",
    tags=["promo"],
    response_model=ResponseSerializer
)
async def upload_image(
    file: UploadFile,
    product_name: str = Form(...)
        ) -> dict:
    """
    Subir una foto para generar los putos

    Args:
        file (UploadFile): Archivo (imagen a subir)
        product_name (str, optional): Nombre del producto

    Raises:
        UserProcessError: Error al subir la foto

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
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
    tags=["campain"],
    response_model=ResponseSerializer)
async def show_registered_users(api_key: str = Header(None)) -> dict:
    """
    Obtener los usuarios están registrados en la promoción

    Args:
        api_key (str, optional): Llave del administrador para el ingreso

    Raises:
        UserProcessError: Descripcion del error

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
    try:
        if API_KEY != api_key:
            raise UserProcessError(
                "User no authorized",
                401
            )
        response = show_registered_users_handler()
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
    "/show-codes",
    tags=["campain"],
    response_model=ResponseSerializer)
async def show_codes(api_key: str = Header(None)) -> dict:
    """
    obtener los códigos se han generado y redimido

    Args:
        api_key (str, optional): Llave del administrador para el ingreso

    Raises:
        UserProcessError: Descripcion del error

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
    try:
        if API_KEY != api_key:
            raise UserProcessError(
                "User no authorized",
                401
            )
        response = show_codes_handler()
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
    "/show-products",
    tags=["campain"],
    response_model=ResponseSerializer)
async def show_most_registered_products(api_key: str = Header(None)) -> dict:
    """
    Obtenemos los 5 productos que más se están registrando

    Args:
        api_key (str, optional): Llave del administrador para el ingreso

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
    try:
        response = show_most_registered_products_handler()
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
    "/show-user-score",
    tags=["promo"],
    response_model=ResponseSerializer)
async def show_user_score() -> dict:
    """
    Obtenemos los puntos del usuario

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
    try:
        response = show_user_score_handler()
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
    "/show-no-validate-image",
    tags=["campain"],
    response_model=ResponseSerializer)
async def show_no_validate_image(api_key: str = Header(None)) -> dict:
    """
     Imágenes que se deben validar manualmente

    Args:
        api_key (str, optional): Llave del administrador para el ingreso

    Raises:
        UserProcessError: Descripción del error

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
    try:
        if API_KEY != api_key:
            raise UserProcessError(
                "User no authorized",
                401
            )
        response = show_no_validate_image_handler()
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
    "/claim-codes/{quantity}",
    tags=["promo"],
    response_model=ResponseSerializer)
async def claim_codes(quantity: int) -> dict:
    """
    - quantity: Codigos a redimir

    Args:
        quantity (int): Codigos a redimir

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """

    try:
        response = claim_codes_handler(quantity)
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
    "/redeem-codes/{code}",
    tags=["campain"],
    response_model=ResponseSerializer)
async def redeem_codes(
    code: str,
    api_key: str = Header(None)
) -> dict:
    """
    Redimir el bono en la tienda

    Args:
        code (str): Bono generado para redimir en la tienda
        api_key (str, optional): Llave del administrador para el ingreso

    Raises:
        UserProcessError: Descripción del error

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
    try:
        if API_KEY != api_key:
            raise UserProcessError(
                "User no authorized",
                401
            )
        response = redeem_codes_handler(code)
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
    "/validate-image/{identifier}",
    tags=["campain"],
    response_model=ResponseSerializer)
async def validate_image(
    identifier: str,
    is_validated: bool,
    api_key: str = Header(None)
) -> dict:
    """
    

    Args:
        identifier (str): Cedula de ciudadania
        is_validated (bool): Para validar la imagen y que los putos sean tomados,
            de lo contrario se restan los putos
        api_key (str, optional): Llave del administrador para el ingreso

    Raises:
        UserProcessError: Descripción del error

    Returns:
        dict:
            data: dict
            status: int
            message: str
    """
    try:
        if API_KEY != api_key:
            raise UserProcessError(
                "User no authorized",
                401
            )
        response = validate_image_handler(identifier, is_validated)
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