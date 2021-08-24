from flask import Blueprint

from app import api_
from app.api.authentication import ns_auth
from app.api.product import ns_product
from app.api.role import ns_role
from app.api.schemas.product import ProductBase
from app.api.users import ns_user

api_bp = Blueprint('api', __name__)

# register namespaces to api
api_.add_namespace(ns_product)
api_.add_namespace(ns_user)
api_.add_namespace(ns_role)
api_.add_namespace(ns_auth)
