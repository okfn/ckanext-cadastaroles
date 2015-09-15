from ckan import authz, logic
from ckan.logic import auth
from ckan.logic.auth.create import resource_create as _resource_create


def cadasta_admin():
    return {'success': False}


cadasta_admin_create = cadasta_admin
cadasta_admin_delete = cadasta_admin
cadasta_admin_list = cadasta_admin


def package_update(context, data_dict):
    user = context.get('user')
    package = logic.auth.get_package_object(context, data_dict)
    if package.owner_org:
        can_create_resources = authz.has_user_permission_for_some_org(
            user,
            'only_create_resources'
        )
        from_resource_create = context.get('from_resource_create', False)
        if from_resource_create and can_create_resources:
            return {'success': True}
        else:
            return {'success': False}
    return auth.update.package_update(context, data_dict)


def resource_create(context, data_dict):
    context['from_resource_create'] = True
    return _resource_create(context, data_dict)


def cadasta_show_relationships(context, data_dict):
    user = context.get('user')
    package = logic.auth.get_package_object(context,
                                            {'id': data_dict['parcel_id']})
    if package.owner_org:
        can_read_relationships = authz.has_user_permission_for_group_or_org(
            package.owner_org,
            user,
            'read_relationship'
        )
        if can_read_relationships:
            return {'success': True}
    return {'success': False}


def cadasta_show_parcel(context, data_dict):
    user = context.get('user')
    package = logic.auth.get_package_object(context, {'id': data_dict['id']})

    if package.owner_org:
        can_read_relationships = authz.has_user_permission_for_group_or_org(
            package.owner_org,
            user,
            'read'
        )
        if can_read_relationships:
            return {'success': True}
    return {'success': False}
