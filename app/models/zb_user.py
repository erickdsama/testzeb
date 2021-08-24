from flask_restx import fields
from sqlalchemy import String, func, Integer
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel


class ZbUser(BaseModel):
    __tablename__ = 'zb_user'

    id = db.Column(Integer, primary_key=True)
    first_name = db.Column(String(length=100))
    last_name = db.Column(String(length=100))
    password = db.Column(String(length=100))
    email = db.Column(String(length=50), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    photo = db.Column(db.String(length=200))
    role = relationship('Role')
    date_registered = db.Column(db.DateTime(timezone=True), server_default=func.now())


user_model_marshal = {
    "id": fields.Integer,
    "first_name": fields.String,
    "last_name": fields.String,
    "email": fields.String,
    "photo": fields.String,
    "role_id": fields.Integer,
    "date_registered": fields.DateTime,
}
