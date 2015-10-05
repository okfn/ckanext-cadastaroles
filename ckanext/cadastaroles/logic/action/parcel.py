from ckan.logic import validate
from ckan.plugins import toolkit

from ckanext.cadastaroles.logic import schema
from ckanext.cadastaroles.logic.action.util import cadasta_api


@validate(schema.cadasta_get_parcels_schema)
def cadasta_show_parcel(context, data_dict):
    '''Make api call to cadasta api show get

    if parcel id is not provided, then if you are a sysadmin all parcels are
    returned

    :param id: the id of the parcel (optional)
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
    parcel_id = data_dict.get('id')
    if parcel_id:
        result = cadasta_api('parcels/{0}'.format(parcel_id), **data_dict)
    else:
        result = cadasta_api('parcels', **data_dict)
    toolkit.check_access('cadasta_show_parcel', context, data_dict)
    return result


@validate(schema.cadasta_get_parcel_detail_schema)
def cadasta_show_parcel_detail(context, data_dict):
    '''Make api call to cadasta api parcel show detail

    :param id: the id of the parcel (optional)
    :type id: str

    :rtype: dict
    '''
    parcel_id = data_dict.get('id')
    toolkit.check_access('cadasta_show_parcel', context, data_dict)
    return cadasta_api('parcels/{0}/details'.format(parcel_id), **data_dict)
