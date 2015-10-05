from ckan.plugins import toolkit

import urlparse

from pylons import config
import requests


def cadasta_api(endpoint, method='GET', *args, **kwargs):
    try:
        api_url = config['ckanext.cadasta.api_url']
    except KeyError:
        raise toolkit.ValidationError(
            toolkit._('ckanext.cadasta.api_url has not been set')
        )
    url = endpoint.format(*args)

    try:
        r = requests.request(method, urlparse.urljoin(api_url, url),
                             params=kwargs)
        result = r.json()
        return result
    except requests.exceptions.RequestException, e:
        raise toolkit.ValidationError(e)
    except ValueError:
        raise toolkit.ValidationError('Failed to decode json from response')
    except (KeyError, IndexError), e:
        raise toolkit.ValidationError('No parcel_id in response', result)
