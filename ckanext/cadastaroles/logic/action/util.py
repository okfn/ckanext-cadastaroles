from ckan.plugins import toolkit

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
        raise toolkit.ValidationError(e)
    except ValueError, e:
        raise toolkit.ValidationError(error_dict={
            'message': 'The response from the cadasta api was not valid JSON',
            'response': r.text,
            'exception': e.message
        })
    except (KeyError, IndexError), e:
        raise toolkit.ValidationError('No parcel_id in response', result)
