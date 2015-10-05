from nose.tools import assert_equal, assert_raises
import responses
from ckan.tests import helpers, factories
from ckan.lib import search
from ckan.plugins import toolkit


class TestCadastaCreateOrganization(object):
    def teardown(self):
        helpers.reset_db()
        search.clear_all()

    @responses.activate
    def test_create(self):
        responses.add(responses.POST, 'http://cadasta.api/organizations',
                      body='{"cadasta_organization_id": 1}',
                      content_type="application/json")
        organization = factories.Organization(id='1')

        result = helpers.call_action(
            'cadasta_create_organization',
            ckan_id=organization['id'],
            ckan_title=organization['title'],
            ckan_description=organization['description'],
        )

        assert_equal({u'cadasta_organization_id': 1}, result)

    def test_create_as_anonymous_user(self):
        organization = factories.Organization(id='1')

        context = {'user': None, 'ignore_auth': False}
        assert_raises(
            toolkit.NotAuthorized,
            helpers.call_action,
            'cadasta_create_organization',
            context=context,
            ckan_id=organization['id'],
            ckan_title=organization['title'],
            ckan_description=organization['description'],
        )
