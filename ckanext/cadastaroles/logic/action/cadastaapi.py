from ckan.plugins import toolkit
from ckanext.cadastaroles.logic.action.util import cadasta_api

import string

from pylons import config


get_api_map = {
    'cadasta_get_project_overview': '/projects/{id}/overview',
    'cadasta_get_activity': '/show_activity',
}


class ActionNotFound(Exception):
    pass


def make_get_cadasta_action(action_name):
    @toolkit.side_effect_free
    def get_cadasta_api(context, data_dict):
        try:
            action = get_api_map[action_name]
        except KeyError, e:
            raise ActionNotFound(e.message)

        # we actually always want to call check access
        # development option that should be removed later
        if toolkit.asbool(config.get('ckanext.cadasta.enforce_permissions',
                                     True)):
            toolkit.check_access(action_name, context, data_dict)

        used_args = [a[1] for a in string.Formatter().parse(action) if a[1]]

        cadasta_dict = data_dict.copy()

        error_dict = {}
        for arg in used_args:
            if arg not in data_dict.keys():
                error_dict[arg] = ['missing value']
            cadasta_dict.pop(arg, None)
        if error_dict:
            raise toolkit.ValidationError(error_dict)

        endpoint = action.format(**data_dict)

        return cadasta_api(endpoint, **cadasta_dict)
    return get_cadasta_api


def get_actions():
    actions = {}
    for action in get_api_map.keys():
        actions[action] = make_get_cadasta_action(action)
    return actions
