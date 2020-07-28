from app.model import User
from extensions.extensions import ma
from marshmallow import fields,validate

class UserSchema(ma.SQLAlchemyAutoSchema):

    email = fields.Email(required=True)
    password = fields.String(required=True, validate=[validate.Length(min=8, max=100)])

    class Meta:
        model = User
        load_instance = True

class UpdateUserSchema(ma.SQLAlchemySchema):

    email = fields.Email()
    password = fields.String(validate=[validate.Length(min=8, max=100)])
