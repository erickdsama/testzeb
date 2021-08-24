from flask_restx import Namespace, abort

from app.api.base_resource import BaseResource
from app.api.schemas import UserBase
from app.models import ZbUser, user_model_marshal
from app.utils.decorators import admin_required

# Define a Namespace user resources
ns_user = Namespace("user", path="/")

user_schema = ns_user.schema_model(UserBase.__name__, UserBase.schema())
user_model = ns_user.model('UserModel', user_model_marshal)


class UsersResource(BaseResource):
    """
        Private resource users allows get all users and post new user
    """
    model = ZbUser
    decorators = [admin_required()]

    @ns_user.marshal_list_with(user_model)
    def get(self):
        users = self.model.filter()
        return users

    @ns_user.marshal_with(user_model)
    @ns_user.expect(user_schema)
    def post(self):
        self.model = ZbUser(**ns_user.payload)
        user = super(UsersResource, self).post()
        return user


class UserResource(BaseResource):
    """
        Private resource user allows edit, view, and delete specific an User
    """
    model = ZbUser
    decorators = [admin_required()]

    @ns_user.marshal_with(user_model)
    def get(self, user_id):
        return super(UserResource, self).get(user_id)

    @ns_user.marshal_with(user_model)
    @ns_user.expect(user_schema)
    def put(self, user_id, data):
        super(UserResource, self).put(user_id, data)

    @ns_user.marshal_with(user_model)
    @ns_user.expect(user_schema)
    def delete(self, user_id) -> None:
        user = self.model.get_by_id(user_id)
        if not user:
            abort(404)
        user.delete()
        return None


# Register the resource to the user namespace
ns_user.add_resource(UsersResource, '/users/',
                     endpoint='users', methods=['GET', 'POST'])
ns_user.add_resource(UserResource, '/user/<int:user_id>',
                     endpoint='user', methods=['GET', 'PUT', 'DELETE'])
