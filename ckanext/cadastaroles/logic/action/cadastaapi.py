from ckan.plugins import toolkit
from ckanext.cadastaroles.logic.action.util import (
    cadasta_get_api,
    cadasta_post_api,
)

from functools import wraps
import string

from pylons import config


default_converter_types = {
    'limit': int,
    'returnGeometry': bool,
    'project_id': int,
}


class CadastaEndpoint(object):
    def __init__(self, url, argument_types=None):
        self.url = url
        if argument_types is None:
            self.argument_types = default_converter_types
        else:
            self.argument_types = argument_types

    def convert_argument(self, argument_name, value):
        try:
            converter = self.argument_types.get(argument_name, str)
            return converter(value)
        except ValueError:
            return value


get_api_map = {
    'cadasta_get_activity': CadastaEndpoint('/show_activity'),
    # 'cadasta_show_relationships': CadastaEndpoint('/show_relationships'),
    # 'cadasta_show_relationships': CadastaEndpoint('/show_relationships/{id}'),

    # 'cadasta_get_organizations': CadastaEndpoint('/organizations'),
    # 'cadasta_get_organization': CadastaEndpoint('/organizations/{id}'),

    'cadasta_get_resources': CadastaEndpoint('/resources'),
    'cadasta_get_parcels_list': CadastaEndpoint('/projects/{id}/parcels_list'),
    'cadasta_get_project_parcel': CadastaEndpoint(
        '/projects/{id}/parcels/{parcel_id}'),
    'cadasta_get_project_overview': CadastaEndpoint('/projects/{id}/overview'),
    'cadasta_get_project_parcel_detail':
        CadastaEndpoint('/projects/{id}/parcels/{parcel_id}/details'),
    'cadasta_get_project_parcel_history':
        CadastaEndpoint('projects/{id}/parcels/{parcel_id}/history'),
    'cadasta_get_project_parcel_relationship_history': CadastaEndpoint(
        '/projects/{id}/parcels/{parcel_id}/show_relationship_history'),
}


post_api_map = {
    'cadasta_create_project': CadastaEndpoint(
        '/projects', {'cadasta_organization_id': int}),
    'cadasta_create_organization': CadastaEndpoint('/organizations'),
}


def identity(action):
    @wraps(action)
    def wrapper(context, data_dict):
        return action(context, data_dict)
    return wrapper


def make_cadasta_action(action, cadasta_endpoint, decorator, cadasta_api_func):
    @decorator
    def get_cadasta_api(context, data_dict):
        # we actually always want to call check access
        # development option that should be removed later
        if toolkit.asbool(config.get('ckanext.cadasta.enforce_permissions',
                                     True)):
            toolkit.check_access(action, context, data_dict)

        string_arguments = [a[1] for a in
                            string.Formatter().parse(cadasta_endpoint.url)
                            if a[1]]

        cadasta_dict = {}
        for k, v in data_dict.items():
            cadasta_dict[k] = cadasta_endpoint.convert_argument(k, v)

        error_dict = {}
        for arg in string_arguments:
            if arg not in data_dict.keys():
                error_dict[arg] = ['Missing value']
            cadasta_dict.pop(arg, None)
        if error_dict:
            raise toolkit.ValidationError(error_dict)

        endpoint = cadasta_endpoint.url.format(**data_dict)

        return cadasta_api_func(endpoint, **cadasta_dict)
    return get_cadasta_api


def get_actions():
    actions = {}
    for action, cadasta_endpoint in get_api_map.items():
        actions[action] = make_cadasta_action(action, cadasta_endpoint,
                                              toolkit.side_effect_free,
                                              cadasta_get_api)
    return actions


def post_actions():
    actions = {}
    for action, cadasta_endpoint in post_api_map.items():
        actions[action] = make_cadasta_action(action, cadasta_endpoint,
                                              identity,
                                              cadasta_post_api)
    return actions
