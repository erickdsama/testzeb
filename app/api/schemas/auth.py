from flask_restx import fields
from pydantic import BaseModel


class LoginBase(BaseModel):
    username: str
    password: str


jwt_marshal_model = {
    "jwt": fields.String
}
