from ckan import plugins
from ckan.config.routing import SubMapper
from ckan.plugins import toolkit
from ckanext.cadastaroles.logic import action, auth
from ckanext.cadastaroles import model


class CadastarolesPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IConfigurable)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)

    # IActions
    def get_actions(self):
        return {
            'cadasta_admin_create': action.cadasta_admin_create,
            'cadasta_admin_delete': action.cadasta_admin_delete,
            'cadasta_admin_list': action.cadasta_admin_list,
            'cadasta_show_relationship': action.cadasta_show_relationship,
            'cadasta_show_parcel': action.cadasta_show_parcel,
            'cadasta_create_project': action.cadasta_create_project,
        }

    # IAuthFunctions
    def get_auth_functions(self):
        return dict((name, function) for name, function
                    in auth.__dict__.items()
                    if callable(function))

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cadastaroles')
        toolkit.add_ckan_admin_tab(config_, 'cadasta_admins', 'Cadasta Admins')

    # IConfigurable
    def configure(self, config):
        model.setup()

    # IRoutes
    def before_map(self, map):
        controller = 'ckanext.cadastaroles.controller:CadastaAdminController'
        with SubMapper(map, controller=controller) as m:
            m.connect('cadasta_admins', '/ckan-admin/cadasta_admins',
                      action='manage', ckan_icon='user')
            m.connect('cadasta_admin_remove',
                      '/ckan-admin/cadasta_admin_remove',
                      action='remove')
        return map

    # IPackageController
    def after_update(self, context, pkg_dict):
        org = toolkit.get_action('organization_show')(
            data_dict={'id': pkg_dict['owner_org']})

        toolkit.get_action('cadatast_create_project')(
            data_dict={
                'ckan_id': pkg_dict['id'],
                'ckan_title': pkg_dict['id'],
                'cadasta_organization_id': org['id']
            }
        )
