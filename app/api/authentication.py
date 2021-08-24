from flask_jwt_extended import create_access_token
from flask_restx import abort, Namespace
from passlib.hash import bcrypt

from app.api.base_resource import BaseResource
from app.api.schemas import UserBase
from app.api.schemas.auth import LoginBase, jwt_marshal_model
from app.models import ZbUser

# Define Auth Namespace
ns_auth = Namespace("auth", path="/")

login_schema = ns_auth.schema_model(LoginBase.__name__, LoginBase.schema())
jwt_model = ns_auth.model('JWTModel', jwt_marshal_model)


class AuthResource(BaseResource):
    """
        Auth Resource allows to get a jwt token
    """
    @ns_auth.expect(login_schema)
    @ns_auth.marshal_with(jwt_model)
    def post(self):
        username = ns_auth.payload.get("username")
        password = ns_auth.payload.get("password")
        user = ZbUser.first(ZbUser.email == username)
        if not user:
            abort(401)
            right_password = bcrypt.verify(password, user.password)
            if not right_password:
                abort(401)
        user_dict = UserBase.from_orm(user)
        access_token = create_access_token(identity=user_dict.json())
        return {"jwt": access_token}


# Register auth resource to auth namespace
ns_auth.add_resource(AuthResource, '/auth',
                     endpoint='auth', methods=['POST'])
