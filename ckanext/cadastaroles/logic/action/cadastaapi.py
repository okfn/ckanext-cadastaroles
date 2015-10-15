from ckan.plugins import toolkit
from ckanext.cadastaroles.logic.action.util import (
    cadasta_api,
    cadasta_get_api,
    cadasta_post_api,
)

from functools import wraps
import string

from pylons import config


get_api_map = {
    'cadasta_get_project_overview': '/projects/{id}/overview',
    'cadasta_get_activity': '/show_activity',
    'cadasta_get_resources': '/resources',
    'cadasta_get_parcels_list': '/projects/{id}/parcels_list',
    'cadasta_get_project_parcel': '/projects/{id}/parcels/{parcel_id}',
    'cadasta_get_project_parcel_detail':
        '/projects/{id}/parcels/{parcel_id}/details',
    'cadasta_get_project_parcel_history':
        'projects/{id}/parcels/{parcel_id}/history',
    'cadasta_get_project_parcel_relationship_history':
        '/projects/{id}/parcels/{parcel_id}/show_relationship_history',
}


post_api_map = {
    'cadasta_create_project': '/projects',
    'cadasta_create_organization': '/organizations',
}


def identity(action):
    @wraps(action)
    def wrapper(context, data_dict):
        return action(context, data_dict)
    return wrapper


def make_cadasta_action(action, action_endpoint, decorator, cadasta_api_func):
    @decorator
    def get_cadasta_api(context, data_dict):
        # we actually always want to call check access
        # development option that should be removed later
        if toolkit.asbool(config.get('ckanext.cadasta.enforce_permissions',
                                     True)):
            toolkit.check_access(action, context, data_dict)

        used_args = [a[1] for a in string.Formatter().parse(action_endpoint)
                     if a[1]]

        cadasta_dict = data_dict.copy()

        error_dict = {}
        for arg in used_args:
            if arg not in data_dict.keys():
                error_dict[arg] = ['missing value']
            cadasta_dict.pop(arg, None)
        if error_dict:
            raise toolkit.ValidationError(error_dict)

        endpoint = action_endpoint.format(**data_dict)

        return cadasta_api_func(endpoint, **cadasta_dict)
    return get_cadasta_api


def get_actions():
    actions = {}
    for action, action_endpoint in get_api_map.items():
        actions[action] = make_cadasta_action(action, action_endpoint,
                                              toolkit.side_effect_free,
                                              cadasta_get_api)
    return actions


def post_actions():
    actions = {}
    for action, action_endpoint in post_api_map.items():
        actions[action] = make_cadasta_action(action, action_endpoint,
                                              identity,
                                              cadasta_post_api)
    return actions
