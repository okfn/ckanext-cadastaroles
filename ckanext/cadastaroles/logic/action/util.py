from ckan.plugins import toolkit

from functools import partial
import urlparse

from pylons import config
import requests


def cadasta_api(endpoint, method='GET', **kwargs):
    try:
        api_url = config['ckanext.cadasta.api_url']
    except KeyError:
        raise toolkit.ValidationError(
            toolkit._('ckanext.cadasta.api_url has not been set')
        )
    try:
        if method == 'GET':
            r = requests.request(method, urlparse.urljoin(api_url, endpoint),
                                params=kwargs)
        elif method == 'POST':
            r = requests.request(method, urlparse.urljoin(api_url, endpoint),
                                data=kwargs)
        result = r.json()
        return result
    except requests.exceptions.RequestException, e:
        error = 'error connection cadasta api: {0}'.format(e.message)
        raise toolkit.ValidationError([error])
    except ValueError, e:
        raise toolkit.ValidationError(error_dict={
            'message': 'The response from the cadasta api was not valid JSON',
            'response': r.text,
            'exception': e.message
        })
    except (KeyError, IndexError), e:
        raise toolkit.ValidationError('No parcel_id in response', result)


def call_api(endpoint, function, param_name, **kwargs):
    try:
        api_url = config['ckanext.cadasta.api_url']
    except KeyError:
        raise toolkit.ValidationError(
            toolkit._('ckanext.cadasta.api_url has not been set')
        )
    try:
        params = {
            param_name: kwargs,
        }
        r = function(urlparse.urljoin(api_url, endpoint), **params)
        result = r.json()
        return result
    except requests.exceptions.RequestException, e:
        error = 'error connection cadasta api: {0}'.format(e.message)
        raise toolkit.ValidationError([error])
    except ValueError, e:
        raise toolkit.ValidationError(error_dict={
            'message': 'The response from the cadasta api was not valid JSON',
            'response': r.text,
            'exception': e.message
        })
    except (KeyError, IndexError), e:
        raise toolkit.ValidationError('No parcel_id in response', result)


cadasta_get_api = partial(call_api, function=requests.get, param_name='params')
cadasta_post_api = partial(call_api, function=requests.post, param_name='data')
