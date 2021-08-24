from flask_restx import abort, Namespace

from app.api.base_resource import BaseResource
from app.api.schemas import RoleBase
from app.models import Role
from app.models.role import role_model_marshal
from app.utils.decorators import admin_required

# define role Namespace
ns_role = Namespace("role", path="/")

role_schema = ns_role.schema_model(RoleBase.__name__, RoleBase.schema())
role_model = ns_role.model('RoleModel', role_model_marshal)


class RolesResource(BaseResource):
    """
        Private resource Roles can show all roles and post new role
        only admins can access to this resource
    """
    model = Role
    method_decorators = [admin_required()]

    @ns_role.marshal_with(role_model)
    def get(self):
        users = self.model.filter()
        return users

    @ns_role.marshal_with(role_model)
    @ns_role.expect(role_schema)
    def post(self):
        self.model = Role(**ns_role.payload)
        role = super(RolesResource, self).post()
        return role


class RoleResource(BaseResource):
    """
        Private resource Role can get specific role, edit and delete
        it's a private Resource only admins can access
    """
    model = Role
    method_decorators = [admin_required()]

    @ns_role.marshal_with(role_model)
    def get(self, role_id):
        return super(RoleResource, self).get(role_id)

    @ns_role.marshal_with(role_model)
    @ns_role.expect(role_schema)
    def put(self, user_id, data):
        return super(RoleResource, self).put(user_id, data)

    def delete(self, user_id) -> None:
        user = self.model.get_by_id(user_id)
        if not user:
            abort(404)
        user.delete()
        return None


# register Resources to Namespace Role
ns_role.add_resource(RolesResource, '/roles/',
                     endpoint='roles', methods=['GET', 'POST'])
ns_role.add_resource(RoleResource, '/role/<int:product_id>',
                     endpoint='role', methods=['GET', 'PUT', 'DELETE'])
