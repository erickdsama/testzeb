import sqlalchemy.exc
from flask_restx import abort

from app import db


class BaseModel(db.Model):
    """
        BaseModel Abstract Model Class with common queries
    """

    __abstract__ = True
    __tablename__ = "base"

    @classmethod
    def first_by(cls, **kwargs) -> db.Model:
        return cls.query.filter_by(**kwargs)

    @classmethod
    def first(cls, *criteria) -> db.Model:
        return cls.query.filter(*criteria).first()

    @classmethod
    def get_by_id(cls, _id: int):
        return cls.query.get(_id)

    @classmethod
    def filter(cls, *criteria):
        return cls.query.filter(*criteria).all()

    @classmethod
    def exists(cls, *criteria):
        return cls.query.filter(criteria).all()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            abort(409, **{"error": "duplicates key"})
        return self

    def update(self, data: dict):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()
        db.session.refresh(self)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
