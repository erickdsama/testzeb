from sqlalchemy import func, Integer

from app import db
from app.models.base_model import BaseModel


class ProductHistory(BaseModel):
    __tablename__ = "product_history"

    id = db.Column(Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    date_registered = db.Column(db.DateTime(timezone=True), server_default=func.now())


class ProductQueryHistory(BaseModel):
    __tablename__ = "product_query_history"

    id = db.Column(Integer, primary_key=True)
    query = db.Column(db.String(length=100), nullable=False)
    date_registered = db.Column(db.DateTime(timezone=True), server_default=func.now())
