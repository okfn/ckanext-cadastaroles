from ckan.tests import helpers, factories
from ckan.lib import search
from ckan.plugins import toolkit

import os
import json

import responses
from nose.tools import assert_equal, assert_raises


class TestGetProjectOverview(object):
    def setup(self):
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'json'))
        filepath = os.path.join(data_dir, 'project_overview.json')

        self.body = open(filepath).read()
        with open(filepath) as stream:
            self.expected = json.load(stream)

    @responses.activate
    def test_get_overview(self):
        responses.add(responses.GET, 'http://cadasta.api/projects/1/overview',
                      body=self.body,
                      content_type="application/json")

        result = helpers.call_action(
            'cadasta_get_project_overview',
            id=1,
        )
        assert_equal(self.expected, result)

    @responses.activate
    def test_get_overview_fails_if_id_not_provided(self):
        responses.add(responses.GET, 'http://cadasta.api/projects/1/overview',
                      body=self.body,
                      content_type="application/json")
        assert_raises(toolkit.ValidationError,
                      helpers.call_action,
                      'cadasta_get_project_overview')
