from _operator import itemgetter

from flask_restx import abort, Namespace

from app.api.base_resource import BaseResource
from app.api.schemas.product import ProductBase
from app.models import Product, ZbUser
from app.models import product_model_marshal
from app.models.role import ROLETYPE
from app.utils.decorators import admin_required, log_product_visits, log_product_queries
from app.utils.elasticsearch import es
from app.utils.notification import notify_product_change

# define namespace
ns_product = Namespace("product", path="/")


# register schema and model (input, output) data from each resource
product_schema = ns_product.schema_model(ProductBase.__name__, ProductBase.schema())
product_model = ns_product.model('ProductModel', product_model_marshal)


class ProductPublicResource(BaseResource):
    """
        Public access resource to get product detail
    """
    model = Product
    decorators = [log_product_visits()]  # log each visit to specific product

    @ns_product.marshal_with(product_model)
    def get(self, product_id):
        product = super(ProductPublicResource, self).get(product_id)
        return product


class ProductsPublicResource(BaseResource):
    """
        Public access resource to query list of products (catalog)
    """
    model = Product
    decorators = [log_product_queries()]  # log every query sent

    def get(self, query) -> list:
        query_body = {
            "query": {
                "simple_query_string": {
                    "query": f'{query}',
                    "fields": ["summary", "brand", "title^3", "long_description"],
                    "auto_generate_synonyms_phrase_query": True
                }
            },
        }
        res = es.search(index="product", body=query_body)
        hits = res.get("hits", {}).get("hits", [])
        # sort the results in order of _score or relevancy
        new_list = sorted(hits, key=itemgetter('_score'), reverse=True)
        return new_list


class ProductsResource(BaseResource):
    """
        Private resource from products only can access Admin users
        allow methods =[POST, GET]
    """
    model = Product
    decorators = [admin_required()]

    @ns_product.marshal_with(product_model)
    @ns_product.expect(product_schema)
    def post(self):
        self.model = Product(**ns_product.payload)
        product = super(ProductsResource, self).post()
        es.index(index='product', id=product.id, body=ns_product.payload, request_timeout=30)
        return product

    @ns_product.marshal_list_with(product_model)
    def get(self):
        products = self.model.filter()
        return products


class ProductResource(BaseResource):
    """
        Private resource from product only can access Admin users
        allow methods =[PUT, GET, DELETE]
    """
    model = Product
    decorators = [admin_required()]

    @ns_product.marshal_with(product_model)
    def get(self, product_id):
        product = super(ProductResource, self).get(product_id)
        return product

    @ns_product.marshal_with(product_model)
    @ns_product.expect(product_schema)
    def put(self, product_id):
        admin_users = ZbUser.filter(ZbUser.role_id == ROLETYPE.ADMIN)
        product = super(ProductResource, self).put(product_id, ns_product.payload)

        # notify if a product is updated to every admin user
        notify_product_change(admin_users, product)
        return product

    def delete(self, product_id):
        product = self.model.get_by_id(product_id)
        if not product:
            abort(404)
        product.delete()
        return None, 204


# register all resources in Namespace of flask_restx
ns_product.add_resource(ProductPublicResource, '/catalog/<int:product_id>/detail',
                        endpoint='catalog-detail', methods=['GET'])
ns_product.add_resource(ProductsPublicResource, '/catalog/<string:query>',
                        endpoint='catalog', methods=['GET'])
ns_product.add_resource(ProductsResource, '/products/',
                        endpoint='products', methods=['GET', 'POST'])
ns_product.add_resource(ProductResource, '/product/<int:product_id>',
                        endpoint='product', methods=['GET', 'PUT', 'DELETE'])
