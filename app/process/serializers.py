from datetime import date
from pydantic import BaseModel


class UserLoginSerializer(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "dajhednde@hayje.co",
                "password": "Sen50reQW0"
            }
        }


class UserSerializer(BaseModel):
    fullname: str
    identification: int
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "fullname": "Laura Sofia Castrinel",
                "identification":  102458744,
                "email": "dajhednde@hayje.co",
                "password": "Sen50reQW0"
            }
        }


class ResponseSerializer(BaseModel):
    data: dict
    status: int
    message: str

    class Config:
        schema_extra = {
            "example": {
                "data": {"name": "Rafael"},
                "status": 200,
                "message": "Exitoso"
            }
        }
