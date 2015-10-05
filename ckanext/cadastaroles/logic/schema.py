from ckan.plugins import toolkit


not_missing = toolkit.get_validator('not_missing')
user_exists = toolkit.get_validator('user_id_or_name_exists')
ignore_missing = toolkit.get_validator('ignore_missing')
int_validator = toolkit.get_validator('int_validator')
boolean_validator = toolkit.get_validator('boolean_validator')


def cadasta_admin_schema():
    return {
        'username': [not_missing, unicode, user_exists],
    }


def cadasta_show_schema():
    return {
        'id': [not_missing, unicode],
        'fields': [ignore_missing, unicode],
        'sort_by': [ignore_missing, unicode],
        'sort_dir': [ignore_missing, unicode],
        'limit': [ignore_missing, int_validator],
        'returnGeometry': [ignore_missing, boolean_validator],
        'project_id': [ignore_missing, int_validator],
    }


def cadasta_get_parcels_schema():
    return {
        'id': [ignore_missing, unicode],
        'fields': [ignore_missing, unicode],
        'sort_by': [ignore_missing, unicode],
        'sort_dir': [ignore_missing, unicode],
        'limit': [ignore_missing, int_validator],
        'returnGeometry': [ignore_missing, boolean_validator],
        'project_id': [ignore_missing, int_validator],
    }


def cadasta_show_relationship_schema():
    return {
        'fields': [ignore_missing, unicode],
        'sort_by': [ignore_missing, unicode],
        'sort_dir': [ignore_missing, unicode],
        'limit': [ignore_missing, int_validator],
        'returnGeometry': [ignore_missing, boolean_validator],
    }


def cadasta_project_schema():
    return {
        'cadasta_organization_id': [not_missing, int_validator],
        'ckan_id': [not_missing, unicode],
        'ckan_title': [not_missing, unicode]
    }


def cadasta_create_organization_schema():
    return {
        'ckan_id': [not_missing, unicode],
        'ckan_title': [not_missing, unicode],
        'ckan_description': [not_missing, unicode],
    }


def cadasta_get_organization_schema():
    return {
        'id': [ignore_missing, unicode],
        'sort_by': [ignore_missing, unicode],
        'sort_dir': [ignore_missing, unicode],
        'limit': [ignore_missing, int_validator],
        'returnGeometry': [ignore_missing, boolean_validator],
    }
