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


def cadasta_show_relationships():
    return {
        'id': [not_missing, unicode],
        'fields': [ignore_missing, unicode],
        'sort_by': [ignore_missing, unicode],
        'sort_dir': [ignore_missing, unicode],
        'limit': [ignore_missing, int_validator],
        'returnGeometry': [ignore_missing, boolean_validator],
    }
