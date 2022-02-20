from app.process.helpers import GeneralHelpers
from app.process.utils import generate_code
from .exceptions import (
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

    @staticmethod
    def count_images_for_date(user_id: str):
        date_from = GeneralHelpers.get_date_from()
        date_to = GeneralHelpers.get_date_to()

        images_qty = ImagesModel.objects(user_id=user_id).filter(
            date__gte=date_from,
            date__lt=date_to
        )
        if images_qty.count() < 5:
            return True
        return False

    @staticmethod
    def show_user():
        return UserModel.objects().count()

    @staticmethod
    def show_codes():
        codes = CodesModel.objects().count()
        redeemed = CodesModel.objects(is_redeemed=True).count()
        return {
            "message": "Codes retrieved successfully",
            "data": {
                "total": codes,
                "redeemed": redeemed
            }
        }

    @staticmethod
    def claim_codes(user_id: str, quantity: int):
        user = PointModel.objects(
            user_id=user_id
        )
        if user.count() == 0:
            raise UserProcessError(
                "This user have not point",
                404
            )
        user = user.get(user_id=user_id)
        score = user.score
        if (score//1000) >= quantity:
            codes: list = [generate_code() for _ in range(quantity)]
            return {"codes": codes}
        return {
            "message": "You don't have enough points, 1 bonus=1000 points",
            "data": {
                "points": score
            }
        }

    @staticmethod
    def save_code(user_id: str, code: str):
        try:
            CodesModel(
                user_id=user_id,
                code=code
            ).save()
            return True
        except Exception as e:
            print(str(e))
            return False

    @staticmethod
    def redeem_code(code: str):
        code_obj = CodesModel.objects(code=code)
        if code_obj == 0:
            raise UserProcessError(
                "This code does not exist",
                404
            )
        code_obj = code_obj.get(code=code)
        if code_obj.is_redeemed:
            raise UserProcessError(
                "This code was redeemed",
                409
            )
        code_obj.is_redeemed = True
        code_obj.save()
        return {
            "message": "this code was redeemed successfully"
        }

    @staticmethod
    def show_user_score(user_id: str):
        user = PointModel.objects(user_id=user_id)
        if user.count() == 0:
            raise UserProcessError(
                "The user doesn't have any point",
                404
            )
        user = user.get(user_id=user_id)
        return {
            "message": f"You have {user.score} point(s)"
        }
