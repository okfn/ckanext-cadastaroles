from ckan import authz, logic


def cadasta_get_parcels(context, data_dict):
    return {'success': True}
    # user = context.get('user')

    # project_id = data_dict.get('project_id')
    # if project_id:
    #     package = logic.auth.get_package_object(context, {'id': project_id})

    #     if package.owner_org:
    #         can_read_parcels = authz.has_user_permission_for_group_or_org(
    #             package.owner_org,
    #             user,
    #             'read_parcel'
    #         )
    #         if can_read_parcels:
    #             return {'success': True}
    # return {'success': False}
