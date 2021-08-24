from flask_restx import fields
from sqlalchemy import String, func, Integer

from app import db
from app.models.base_model import BaseModel


class Product(BaseModel):
    __tablename__ = "product"
    id = db.Column(Integer, primary_key=True, autoincrement=True)
    title = db.Column(String(length=50))
    sku = db.Column(db.String(length=24),  unique=True, nullable=False)
    summary = db.Column(db.String(length=200))
    photo = db.Column(db.String(length=200))
    brand = db.Column(db.String(length=30), index=True, nullable=False)
    long_description = db.Column(db.String)
    date_registered = db.Column(db.DateTime(timezone=True), server_default=func.now())


product_model_marshal = {
    "id": fields.Integer,
    "title": fields.String,
    "sku": fields.String,
    "summary": fields.String,
    "photo": fields.String,
    "brand": fields.String,
    "long_description": fields.String,
    "date_registered": fields.DateTime,
}
