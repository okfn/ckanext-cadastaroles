from ckan import model
from ckan.logic import validate
from ckan.plugins import toolkit
from ckanext.cadastaroles.logic import schema
from ckanext.cadastaroles.model import CadastaAdmin


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
