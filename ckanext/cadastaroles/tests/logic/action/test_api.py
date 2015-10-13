from ckan.tests import helpers
from ckan.plugins import toolkit

from ckanext.cadastaroles.logic.action.cadastaapi import get_api_map

import os
import json
import string
from urlparse import urljoin

from pylons import config
import responses
from nose.tools import assert_equal, assert_raises


class TestGetApi(object):
    def setup(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     'json'))
        self.test_api = config['ckanext.cadasta.api_url']

    @responses.activate
    def test_all_get_actions_success(self):
        for action, api_url in get_api_map.items():
            print 'testing {action}'.format(action=action),
            # read our expected json output as <action_name>.json
            filepath = os.path.join(self.data_dir, '.'.join([action, 'json']))
            body = open(filepath).read()
            expected = json.loads(body)

            # add the expected parameters (everything is a 1)
            url_args = dict([(a[1], 1) for
                             a in string.Formatter().parse(api_url) if a[1]])

            # make sure the point parameters are filled out
            endpoint = urljoin(self.test_api, api_url).format(**url_args)

            # fake out our response
            responses.add(responses.GET, endpoint,
                          body=body,
                          content_type="application/json")

            # call our action with the same arguments passed
            result = helpers.call_action(action, **url_args)
            assert_equal(expected, result)
            print '\t[OK]'

    @responses.activate
    def test_all_no_parameters_fail(self):
        for action, api_url in get_api_map.items():
            print 'testing {action}'.format(action=action),
            # read our expected json output as <action_name>.json
            filepath = os.path.join(self.data_dir, '.'.join([action, 'json']))
            body = open(filepath).read()

            # add the expected parameters (everything is a 1)
            url_args = dict([(a[1], 1) for
                             a in string.Formatter().parse(api_url) if a[1]])

            # if this endpoint needs no parameters, quit early, test does not
            # apply
            if not url_args:
                return

            # make sure the point parameters are filled out
            endpoint = urljoin(self.test_api, api_url).format(**url_args)

            # fake out our response
            responses.add(responses.GET, endpoint,
                          body=body,
                          content_type="application/json")

            # call our action with no arguments
            assert_raises(toolkit.ValidationError, helpers.call_action, action)
            print '\t[OK]'
