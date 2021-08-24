from flask_restx import Resource, abort

from app.models.base_model import BaseModel


class BaseResource(Resource):
    """
        BaseResource is used in many Resources
    """
    model: BaseModel = None

    def post(self):
        self.model.save()
        return self.model

    def put(self, product_id, data):
        product = self.model.get_by_id(product_id)
        if not product:
            abort(404)
        product.update(data=data)
        return product

    def get(self, product_id):
        product = self.model.get_by_id(product_id)
        if not product:
            abort(404)
        return product
