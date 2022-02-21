from app.process.helpers import GeneralHelpers
from app.process.utils import generate_code, get_dict_from_list, sort_dict
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
        return images_qty.count()

    @staticmethod
    def show_user():
        user_qty = UserModel.objects().count()
        return {
            "message": f"There are {user_qty} registered user(s)"
        }

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

    @staticmethod
    def show_no_validate_image():
        validate_images = ImagesModel.objects(is_checked=False)
        if validate_images.count() == 0:
            return {
                "message": "There is not any image to be validated"
            }
        return {
            "message": "These images have not been validated",
            "data": {
                "Image_code": [{
                    "identifier": image.identifier,
                    "score": image.score
                }
                    for image in validate_images
                ],
                "quantity": validate_images.count()
            }
        }

    @staticmethod
    def validate_image(identifier: str, is_validated: bool):
        image_obj = ImagesModel.objects(identifier=identifier)
        if image_obj == 0:
            raise UserProcessError(
                "This image does not exist",
                404
            )
        image_obj = image_obj.get(identifier=identifier)
        if image_obj.is_checked:
            raise UserProcessError(
                "This image was checked",
                409
            )
        image_obj.is_checked = True
        image_obj.is_validated = is_validated
        image_obj.save()
        Queryset.update_user_score(
            user_id=image_obj.user_id,
            score=-image_obj.score
        )
        return {
            "message": "this image was checked successfully"
        }

    @staticmethod
    def get_most_used_product():
        product_obj: list = ImagesModel.objects()
        if product_obj == 0:
            raise UserProcessError(
                "There are any product registered",
                404
            )
        products = [product.product_name for product in product_obj]
        products_dict = get_dict_from_list(products)
        most_used_products = sort_dict(products_dict)[:6]
        return {
            "message": "These are the most used product",
            "data": {
                "Product": most_used_products
            }
        }
