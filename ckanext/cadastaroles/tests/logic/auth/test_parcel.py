import responses
from ckan.tests import helpers, factories
from ckan.lib import search
from ckan.plugins import toolkit
from nose.tools import assert_raises


class TestCadastaParcel(object):
    def teardown(self):
        helpers.reset_db()
        search.clear_all()

    @responses.activate
    def test_cadasta_show_parcel(self):
        body = '{"test": "test"}'
        user = factories.User()
        responses.add(responses.GET, 'http://cadasta.api/parcels/1',
                      body=body,
                      content_type="application/json")

        context = {'user': user['name'], 'ignore_auth': False}
        helpers.call_action(
            'cadasta_show_parcel',
            context=context,
            id=1,
        )

    def test_cadasta_show_parcel_anon_raises_validation_error(self):
        body = '{"test": "test"}'
        responses.add(responses.GET, 'http://cadasta.api/parcels/1',
                      body=body,
                      content_type="application/json")

        context = {'user': None, 'ignore_auth': False}
        assert_raises(
            toolkit.ValidationError,
            helpers.call_action,
            'cadasta_show_parcel',
            context=context,
            id=1,
        )
