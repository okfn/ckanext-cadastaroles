from ckan.plugins import toolkit


def cadasta_create_project(context, data_dict):
    return toolkit.check_access('package_create', context, data_dict={
        'id': data_dict['ckan_id']})
