from .exceptions import (
    TooMuchImagesError,
    UserProcessError
)
from .models import (
    CodesModel,
    ImagesModel,
    PointModel,
    UserModel
)


class Queryset:

    @staticmethod
    def create_user(data: dict):
        user = UserModel.objects(identification=data["identification"]) or\
            UserModel.objects(email=data["email"])
        if user.count() != 0:
            raise UserProcessError(
                "There is a user with this identification or email",
                409
            )
        UserModel(**data).save()

        return {"message": "The user was created successfully"}

    @staticmethod
    def login_user(data: dict):
        user = UserModel.objects(
            email=data["email"],
            password=data["password"]
            )
        if user.count() == 0:
            raise UserProcessError(
                "Invalited credential, wrong email or passsword",
                400
            )

        return {
            "message": "Login successfully",
            "data": {
                "user_id": user[0].identifier
            }
        }
