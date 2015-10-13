from ckan.tests import helpers

import os
import json

import responses
from nose.tools import assert_equal


class TestGetActivity(object):
    def setup(self):
        data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'json'))
        filepath = os.path.join(data_dir, 'show_activity.json')

        self.body = open(filepath).read()
        with open(filepath) as stream:
            self.expected = json.load(stream)

    @responses.activate
    def test_get_activity(self):
        responses.add(responses.GET, 'http://cadasta.api/show_activity',
                      body=self.body,
                      content_type="application/json")

        result = helpers.call_action(
            'cadasta_get_activity',
        )
        assert_equal(self.expected, result)
