from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.cadastaroles.logic import schema
from ckanext.cadastaroles.logic.action.util import cadasta_api


@validate(schema.cadasta_create_organization_schema)
def cadasta_create_organization(context, data_dict):
    '''Make api call to cadasta-api create organization

    You must be a sysadmin to create organizations

    :param ckan_id: dataset(project) id in ckan
    :type ckan_id: str
    :param ckan_title: title of the ckan dataset
    :type ckan_title: str
    :param ckan_description: description of the ckan dataset
    :type ckan_title: str

    :rtype: dict
    '''
    toolkit.check_access('sysadmin', context, data_dict)
    return cadasta_api('organizations', 'POST', data_dict)
