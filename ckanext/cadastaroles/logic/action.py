from ckan import model
from ckan.logic import validate
from ckan.plugins import toolkit
from ckanext.cadastaroles.logic import schema
from ckanext.cadastaroles.model import CadastaAdmin

import json
import urlparse

from pylons import config
import requests


@validate(schema.cadasta_admin_schema)
def cadasta_admin_create(context, data_dict):
    toolkit.check_access('cadasta_admin_create', context, data_dict)
    session = context['session']
    username = data_dict['username']
    user_object = model.User.get(username)
    if CadastaAdmin.exists(session, user_id=user_object.id):
        raise toolkit.ValidationError(
            'user {0} is already a Cadasta admin'.format(username)
        )
    return CadastaAdmin.create(session, user_id=user_object.id)


@validate(schema.cadasta_admin_schema)
def cadasta_admin_delete(context, data_dict):
    toolkit.check_access('cadasta_admin_delete', context, data_dict)
    session = context['session']
    username = data_dict['username']
    user_object = model.User.get(username)
    admin = CadastaAdmin.get(session, user_id=user_object.id)
    if admin:
        session.delete(admin)
        session.commit()
    else:
        raise toolkit.ValidationError(
            'user {0} is not a Cadasta admin'.format(username)
        )


def cadasta_admin_list(context, data_dict):
    toolkit.check_access('cadasta_admin_list', context, data_dict)
    session = context['session']
    user_ids = CadastaAdmin.get_cadasta_admin_ids(session)
    return [toolkit.get_action('user_show')(data_dict={'id': user_id})
            for user_id in user_ids]


@validate(schema.cadasta_show_schema)
def cadasta_show_relationship(context, data_dict):
    relationship_id = data_dict.get('id', '')
    result = cadasta_api('show_relationships/{0}', relationship_id, data_dict)
    auth_dict = data_dict
    auth_dict['parcel_id'] = str(result['features'][0]['properties']['parcel_id'])
    toolkit.check_access('cadasta_show_relationships', context, data_dict)
    return result


@validate(schema.cadasta_show_schema)
def cadasta_show_parcel(context, data_dict):
    parcel_id = data_dict.get('id',  '')
    result = cadasta_api('parcels/{0}', parcel_id, data_dict)
    toolkit.check_access('cadasta_show_parcel', context, data_dict)
    return result


def cadasta_api(endpoint, *args, **kwargs):
    api_url = config.get('ckanext.cadasta.api_url', '')
    url = endpoint.format(*args)

    try:
        r = requests.get(urlparse.urljoin(api_url, url), params=kwargs)
        result = r.json()
        return result
    except requests.exceptions.RequestException, e:
        raise toolkit.ValidationError(e)
    except ValueError:
        raise toolkit.ValidationError('Failed to decode json from response')
    except (KeyError, IndexError), e:
        raise toolkit.ValidationError('No parcel_id in response', result)
