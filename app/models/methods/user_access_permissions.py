from app.models.user_access_permissions import User_Access_Permissions


class Methods_User_Access_Permissions:
    @classmethod
    def get_access_permissions(cls, id):
        access_permissions = User_Access_Permissions.objects.filter(users_user_id=id)
        auth_permissions = {}
        counter = 0
        for access_permission in access_permissions:
            auth_permissions[
                counter
            ] = (
                access_permission.access_permissions_access_permission_name.access_permission_name
            )
            counter = counter + 1
        return auth_permissions
