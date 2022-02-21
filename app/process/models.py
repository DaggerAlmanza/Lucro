from mongoengine import Document
from mongoengine.fields import (
    BooleanField,
    DateTimeField,
    EmbeddedDocument,
    EmbeddedDocumentListField,
    IntField,
    StringField
)

from app.process.helpers import GeneralHelpers


class CodeDocument(EmbeddedDocument):
    code = StringField(required=True)
    is_redeemed = BooleanField(required=True)


class UserModel(Document):
    identifier = StringField(
        default=lambda: GeneralHelpers.get_uuid(),
        unique=True
    )
    fullname = StringField(required=True)
    identification = IntField(required=True, unique=True)
    email = StringField(required=True, unique=True)
    password = StringField(required=True)
    date = DateTimeField(
        default=lambda: GeneralHelpers.get_datetime(),
    )


class PointModel(Document):
    identifier = StringField(
        default=lambda: GeneralHelpers.get_uuid(),
        unique=True
    )
    user_id = StringField(required=True)
    score = IntField(required=True)
    codes = EmbeddedDocumentListField(CodeDocument)
    date = DateTimeField(
        default=lambda: GeneralHelpers.get_datetime(),
    )


class CodesModel(Document):
    identifier = StringField(
        default=lambda: GeneralHelpers.get_uuid(),
        unique=True
    )
    user_id = StringField(required=True)
    code = StringField(required=True)
    is_redeemed = BooleanField(default=False)
    date = DateTimeField(
        default=lambda: GeneralHelpers.get_datetime(),
    )


class ImagesModel(Document):
    identifier = StringField(
        default=lambda: GeneralHelpers.get_uuid(),
        unique=True
    )
    user_id = StringField(required=True)
    product_name = StringField(required=True)
    score = IntField(required=True)
    is_validated = BooleanField(default=True)
    is_checked = BooleanField(required=True)
    date = DateTimeField(
        default=lambda: GeneralHelpers.get_datetime(),
    )
