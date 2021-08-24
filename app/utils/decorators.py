import json
from functools import wraps
from os import abort

from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask_restx import abort

from app.models import ProductHistory
from app.models.product_history import ProductQueryHistory
from app.models.role import ROLETYPE


def admin_required():
    """
    Admin required decorator, check if user has role Admin
    if haven't Admin role can't access to certain Resources
    @return:
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            identity = get_jwt_identity()
            identity_json = json.loads(identity)
            role_id = int(identity_json.get("role_id", {}))
            if role_id == ROLETYPE.ADMIN:
                return fn(*args, **kwargs)
            else:
                return abort(403, "only Admin can modified this recource")
        return decorator
    return wrapper


def log_product_visits():
    """
    log every visit in the detail page of products
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            product_history = ProductHistory(product_id=kwargs.get("product_id"))
            product_history.save()
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def log_product_queries():
    """
    log every query maybe with more data we can improve better results
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            product_history = ProductQueryHistory(query=kwargs.get("query"))
            product_history.save()
            return fn(*args, **kwargs)
        return decorator
    return wrapper
