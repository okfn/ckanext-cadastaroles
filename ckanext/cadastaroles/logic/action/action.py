from ckan.logic import validate
from ckan.plugins import toolkit
from ckanext.cadastaroles.logic import schema

import urlparse

from pylons import config
import requests


@validate(schema.cadasta_show_relationship_schema)
def cadasta_show_relationship(context, data_dict):
    '''Make api call to cadasta api show relationship

    :param fields: Options: id, spatial_source, user_id, time_created,
        time_updated
    :type fields: str
    :param sort_dir: optional (ASC or DESC)
    :type fields: str
    :param limit: number of records to return
    :type limit: int
    :param returnGeometry: whether to return geometry (optional,
        default: false)
    :type returnGeometry: boolean

    :rtype: dict
    '''
    relationship_id = data_dict.get('id', '')
    result = cadasta_api('show_relationships/{0}', relationship_id, data_dict)
    auth_dict = data_dict
    auth_dict['parcel_id'] = str(
        result['features'][0]['properties']['parcel_id'])
    toolkit.check_access('cadasta_show_relationships', context, data_dict)
    return result


@validate(schema.cadasta_show_schema)
def cadasta_show_parcel(context, data_dict):
    '''Make api call to cadasta api show parcel

    :param id: the id of the project
    :type id: str
    :param fields: Options: id, spatial_source, user_id, time_created,
        time_updated
    :type fields: str
    :param sort_dir: optional (ASC or DESC)
    :type fields: str
    :param limit: number of records to return
    :type limit: int
    :param returnGeometry: whether to return geometry (optional,
        default: false)
    :type returnGeometry: boolean
    :param project_id: project id the parcel belongs to (optional)
    :type project_id: int

    :rtype: dict
    '''
    parcel_id = data_dict.get('id',  '')
    result = cadasta_api('parcels/{0}', parcel_id, data_dict)
    toolkit.check_access('cadasta_show_parcel', context, data_dict)
    return result


@validate(schema.cadasta_show_parcels_schema)
def cadasta_show_parcels(context, data_dict):
    '''Make api call to cadasta api show parcels

    :param fields: Options: id, spatial_source, user_id, time_created,
        time_updated
    :type fields: str
    :param sort_dir: optional (ASC or DESC)
    :type fields: str
    :param limit: number of records to return
    :type limit: int
    :param returnGeometry: whether to return geometry (optional,
        default: false)
    :type returnGeometry: boolean
    :param project_id: project id the parcel belongs to (optional)
    :type project_id: int

    :rtype: dict
    '''
    parcel_id = data_dict.get('id',  '')
    result = cadasta_api('parcels/{0}', parcel_id, data_dict)
    toolkit.check_access('cadasta_show_parcel', context, data_dict)
    return result


@validate(schema.cadasta_project_schema)
def cadasta_create_project(context, data_dict):
    '''Make api call to cadasta-api create project

    You must be an organization admin in order to create projects.

    :param cadasta_organization_id: The cadasta id of the project's "parent"
    :type cadasta_organization_id: int
    :param ckan_id: dataset(project) id in ckan
    :type ckan_id: str
    :param ckan_title: title of the ckan dataset
    :type ckan_title: str

    :rtype: dict
    '''
    toolkit.check_access('cadasta_create_project', context, data_dict)
    return cadasta_api('projects', 'POST', data_dict)


def cadasta_api(endpoint, method='GET', *args, **kwargs):
    try:
        api_url = config['ckanext.cadasta.api_url']
    except KeyError:
        raise toolkit.ValidationError(
            toolkit._('ckanext.cadasta.api_url has not been set')
        )
    url = endpoint.format(*args)

    try:
        r = requests.request(method, urlparse.urljoin(api_url, url),
                             params=kwargs)
        result = r.json()
        return result
    except requests.exceptions.RequestException, e:
        raise toolkit.ValidationError(e)
    except ValueError:
        raise toolkit.ValidationError('Failed to decode json from response')
    except (KeyError, IndexError), e:
        raise toolkit.ValidationError('No parcel_id in response', result)
