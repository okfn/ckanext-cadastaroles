'''This module monkey patches functions in ckan/authz.py and replaces the
default roles with custom roles and decorates
has_user_permission_for_group_org_org to allow a CadastaAdmin to admin groups,
CadastaAdmins can manage all organizations/groups, but have no other sysadmin
powers
'''
from ckan import authz, model
from ckan.common import OrderedDict
from ckan.plugins import toolkit
from ckanext.cadastaroles.model import CadastaAdmin


authz.ROLE_PERMISSIONS = OrderedDict([
    ('admin', ['admin']),
    ('community_admin', ['read',
                         'delete_dataset',
                         'create_dataset',
                         'update_dataset',
                         # cadasta resources
                         'read_cadasta_resource',
                         'create_cadasta_resource',
                         'update_cadasta_resource',
                         'delete_cadasta_resource',
                         # surveys
                         'read_survey',
                         'create_survey',
                         'update_survey',
                         'delete_survey',
                         # parcel
                         'read_parcel',
                         'create_parcel',
                         'update_parcel',
                         'delete_parcel',
                         # relationship
                         'read_relationship',
                         'create_relationship',
                         'update_relationship',
                         'delete_relationship',
                         # group membership
                         'manage_group'
                         ]),
    ('community_user', ['read',
                        # cadasta resources
                        'read_cadasta_resource',
                        'create_cadasta_resource',
                        'update_cadasta_resource',
                        'delete_cadasta_resource',

                        'read_survey',

                        'read_parcel',

                        'read_relationship',
                        ]),
    ('surveyor', ['read',

                  'read_survey',
                  'create_survey',
                  'update_survey',
                  'delete_survey',

                  'read_parcel',
                  'create_parcel',
                  'update_parcel',
                  'delete_parcel',

                  'read_relationship',
                  'create_relationship',
                  'update_relationship',
                  'delete_relationship',
                  ]),
])


def _trans_role_surveyor():
    return toolkit._('Surveyor')


def _trans_role_community_admin():
    return toolkit._('Community Admin')


def _trans_role_community_user():
    return toolkit._('Community User')


authz._trans_role_surveyor = _trans_role_surveyor
authz._trans_role_community_admin = _trans_role_community_admin
authz._trans_role_community_user = _trans_role_community_user


def is_cadasta_admin_decorator(method):
    def decorate_has_user_permission_for_group_or_org(group_id, user_name,
                                                      permission):
        user_id = authz.get_user_id_for_username(user_name, allow_none=True)
        if not user_id:
            return False
        if CadastaAdmin.is_user_cadasta_admin(model.Session, user_id):
            return True
        return method(group_id, user_name, permission)
    return decorate_has_user_permission_for_group_or_org


authz.has_user_permission_for_group_or_org = is_cadasta_admin_decorator(
    authz.has_user_permission_for_group_or_org)
