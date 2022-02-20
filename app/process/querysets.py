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

    @staticmethod
    def register_image(
        user_id: str,
        product_name: str,
        score: int,
        is_checked: bool
    ):
        ImagesModel(
            user_id=user_id,
            product_name=product_name,
            score=score,
            is_checked=is_checked
        ).save()

    @staticmethod
    def update_user_score(user_id: str, score: int) -> dict:
        transaction = PointModel.objects(
                user_id=user_id
            )
        if transaction.count() == 0:
            PointModel(
                user_id=user_id,
                score=score
            ).save()
        else:
            transaction = transaction.get(user_id=user_id)
            transaction.score += score
            transaction.save()
