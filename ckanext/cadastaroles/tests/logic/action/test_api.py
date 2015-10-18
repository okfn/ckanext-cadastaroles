from ckan.tests import helpers
from ckan.plugins import toolkit

from ckanext.cadastaroles.logic.action.api import (
    get_api_map,
    post_api_map,
    post_files_api_map,
)

import os
import json
import string
from urlparse import urljoin
from cStringIO import StringIO

from pylons import config
import responses
from nose.tools import assert_equal, assert_raises, assert_in


class TestGetApi(object):
    def setup(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     'json'))
        self.test_api = config['ckanext.cadasta.api_url']

    @responses.activate
    def test_all_get_actions_success(self):
        for action, cadasta_endpoint in get_api_map.items():
            print 'testing {action}'.format(action=action),
            # read our expected json output as <action_name>.json
            filepath = os.path.join(self.data_dir, '.'.join([action, 'json']))
            body = open(filepath).read()
            expected = json.loads(body)

            # add the expected parameters (everything is a 1)
            api_url = cadasta_endpoint.url
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
        for action, cadasta_endpoint in get_api_map.items():
            print 'testing {action}'.format(action=action),
            # read our expected json output as <action_name>.json
            filepath = os.path.join(self.data_dir, '.'.join([action, 'json']))
            body = open(filepath).read()

            # add the expected parameters (everything is a 1)
            api_url = cadasta_endpoint.url
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


class TestPostApi(object):
    def setup(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     'json'))
        self.test_api = config['ckanext.cadasta.api_url']

    @responses.activate
    def test_all_post_actions_success(self):
        for action, cadasta_endpoint in post_api_map.items():
            print 'testing {action}'.format(action=action),
            # read our expected json output as <action_name>.json
            filepath = os.path.join(self.data_dir, '.'.join([action, 'json']))
            body = open(filepath).read()
            expected = json.loads(body)

            # add the expected parameters (everything is a 1)
            api_url = cadasta_endpoint.url
            url_args = dict([(a[1], 1) for
                             a in string.Formatter().parse(api_url) if a[1]])

            # make sure the point parameters are filled out
            endpoint = urljoin(self.test_api, api_url).format(**url_args)

            # fake out our response
            responses.add(responses.POST, endpoint,
                          body=body,
                          content_type="application/json")

            # call our action with the same arguments passed
            result = helpers.call_action(action, **url_args)
            assert_equal(expected, result)
            print '\t[OK]'

    @responses.activate
    def test_all_no_parameters_fail(self):
        for action, cadasta_endpoint in post_api_map.items():
            print 'testing {action}'.format(action=action),
            # read our expected json output as <action_name>.json
            filepath = os.path.join(self.data_dir, '.'.join([action, 'json']))
            body = open(filepath).read()

            # add the expected parameters (everything is a 1)
            api_url = cadasta_endpoint.url
            url_args = dict([(a[1], 1) for
                             a in string.Formatter().parse(api_url) if a[1]])

            # if this endpoint needs no parameters, quit early, test does not
            # apply
            if not url_args:
                return

            # make sure the point parameters are filled out
            endpoint = urljoin(self.test_api, api_url).format(**url_args)

            # fake out our response
            responses.add(responses.POST, endpoint,
                          body=body,
                          content_type="application/json")

            # call our action with no arguments
            assert_raises(toolkit.ValidationError, helpers.call_action, action)
            print '\t[OK]'


class TestPostFilesApi(object):
    def setup(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                     'json'))
        self.test_api = config['ckanext.cadasta.api_url']

    @responses.activate
    def test_all_post_actions_success(self):
        for action, cadasta_endpoint in post_files_api_map.items():
            print 'testing {action}'.format(action=action),
            # read our expected json output as <action_name>.json
            filepath = os.path.join(self.data_dir, '.'.join([action, 'json']))
            body = open(filepath).read()
            expected = json.loads(body)

            # add the expected parameters (everything is a 1)
            api_url = cadasta_endpoint.url
            url_args = dict([(a[1], 1) for
                             a in string.Formatter().parse(api_url) if a[1]])

            # make sure the point parameters are filled out
            endpoint = urljoin(self.test_api, api_url).format(**url_args)

            # fake out our response
            responses.add(responses.POST, endpoint,
                          body=body,
                          content_type="application/json")

            if cadasta_endpoint.upload_fields:
                for upload_field in cadasta_endpoint.upload_fields:
                    url_args[upload_field] = StringIO('test file')

            # call our action with the same arguments passed
            result = helpers.call_action(action, **url_args)

            # check a file upload was sent
            assert_in(
                'Content-Disposition: form-data; name="filedata"; '
                'filename="filedata"\r\n\r\ntest file',
                responses.calls[0].request.body
            )
            assert_equal(expected, result)

            print '\t[OK]'

    @responses.activate
    def test_all_no_parameters_fail(self):
        for action, cadasta_endpoint in post_files_api_map.items():
            print 'testing {action}'.format(action=action),
            # read our expected json output as <action_name>.json
            filepath = os.path.join(self.data_dir, '.'.join([action, 'json']))
            body = open(filepath).read()

            # add the expected parameters (everything is a 1)
            api_url = cadasta_endpoint.url
            url_args = dict([(a[1], 1) for
                             a in string.Formatter().parse(api_url) if a[1]])

            # if this endpoint needs no parameters, quit early, test does not
            # apply
            if not url_args:
                return

            # make sure the point parameters are filled out
            endpoint = urljoin(self.test_api, api_url).format(**url_args)

            # fake out our response
            responses.add(responses.POST, endpoint,
                          body=body,
                          content_type="application/json")

            # call our action with no arguments
            assert_raises(toolkit.ValidationError, helpers.call_action, action)
            print '\t[OK]'
