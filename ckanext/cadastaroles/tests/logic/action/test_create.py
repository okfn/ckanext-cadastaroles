from nose.tools import assert_equal
import responses
from ckan.tests import helpers, factories
from ckan.lib import search


class TestCadastaCreateProject(object):
    def teardown(self):
        helpers.reset_db()
        search.clear_all()

    @responses.activate
    def test_create(self):
        responses.add(responses.POST, 'http://cadasta.api/projects',
                      body='{"cadasta_project_id": 1}',
                      content_type="application/json")
        organization = factories.Organization(id='1')
        project = factories.Dataset(owner_org=organization['name'])

        result = helpers.call_action(
            'cadasta_create_project',
            cadasta_organization_id=organization['id'],
            ckan_id=project['id'],
            ckan_title=project['title']
        )

        assert_equal({u'cadasta_project_id': 1}, result)
