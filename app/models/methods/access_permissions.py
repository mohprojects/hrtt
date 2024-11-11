from app.models import Access_Permissions


class Methods_Access_Permissions:
    @classmethod
    def get_access_permissions(cls):
        access_permissions = Access_Permissions.objects.all()
        auth_permissions = {}
        counter = 0
        for access_permission in access_permissions:
            auth_permissions[counter] = access_permission.access_permission_name
            counter = counter + 1
        return auth_permissions
