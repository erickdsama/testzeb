from flask_restx import fields
from sqlalchemy import String, Integer

from app import db
from app.models.base_model import BaseModel


class ROLETYPE:
    ADMIN = 1
    CLIENT = 2
    ANONYMOUS = 0


class Role(BaseModel):
    __tablename__ = 'role'

    id = db.Column(Integer, primary_key=True)
    name = db.Column(String(length=100))


role_model_marshal = {
    "id": fields.Integer,
    "name": fields.String,
}
