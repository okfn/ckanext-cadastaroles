from ckan.tests import helpers, factories
from ckan.lib import search

import os
import json

import responses
from nose.tools import assert_equal


class TestGetProjectOverview(object):
    @responses.activate
    def test_get_overview(self):
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'json'))
        filepath = os.path.join(data_dir, 'project_overview.json')

        responses.add(responses.GET, 'http://cadasta.api/projects/1/overview',
                      body=open(filepath).read(),
                      content_type="application/json")

        result = helpers.call_action(
            'cadasta_get_project_overview',
            id=1,
        )

        with open(filepath) as stream:
            expected = json.load(stream)

        assert_equal(expected, result)
