from ckan.logic import validate
from ckan.plugins import toolkit
from ckanext.cadastaroles.logic import schema
from ckanext.cadastaroles.logic.action.util import cadasta_api


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
    return cadasta_api('projects', 'POST', **data_dict)
