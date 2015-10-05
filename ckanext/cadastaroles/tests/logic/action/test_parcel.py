from nose.tools import assert_equal
import responses
from ckan.tests import helpers
from ckan.lib import search


class TestCadastaGetParcel(object):
    def teardown(self):
        helpers.reset_db()
        search.clear_all()

    @responses.activate
    def test_get_one(self):
        body = '''
            {
                "type": "FeatureCollection",
                "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [
                                    -105.228338241577,
                                    21.1714137482368
                                ],
                                [
                                    -105.229024887085,
                                    21.1694127979643
                                ],
                                [
                                    -105.228338241577,
                                    21.1714137482368
                                ]
                            ]
                        ]
                    },
                    "properties": {
                        "id": 1,
                        "spatial_source": 4,
                        "user_id": "1",
                        "area": null,
                        "land_use": null,
                        "gov_pin": null,
                        "active": true,
                        "time_created": "2015-08-06T15:41:26.440037-07:00",
                        "time_updated": null,
                        "created_by": 1,
                        "updated_by": null
                    }
                } ]
            }
        '''
        responses.add(responses.GET, 'http://cadasta.api/parcels/1',
                      body=body,
                      content_type="application/json")

        result = helpers.call_action(
            'cadasta_show_parcel',
            id=1,
            project_id=1,
        )

        assert_equal({
            u'features': [{
                u'geometry': {
                    u'coordinates': [[[-105.228338241577,
                                       21.1714137482368],
                                      [-105.229024887085,
                                       21.1694127979643],
                                      [-105.228338241577,
                                       21.1714137482368]]],
                    u'type': u'Polygon'},
                u'properties': {
                    u'active': True,
                    u'area': None,
                    u'created_by': 1,
                    u'gov_pin': None,
                    u'id': 1,
                    u'land_use': None,
                    u'spatial_source': 4,
                    u'time_created': u'2015-08-06T15:41:26.440037-07:00',
                    u'time_updated': None,
                    u'updated_by': None,
                    u'user_id': u'1'},
                u'type': u'Feature'
            }],
            u'type': u'FeatureCollection'
            },
            result
        )


    @responses.activate
    def test_get_all(self):
        body = '''
            {
                "type": "FeatureCollection",
                "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [
                                    -105.228338241577,
                                    21.1714137482368
                                ],
                                [
                                    -105.229024887085,
                                    21.1694127979643
                                ],
                                [
                                    -105.228338241577,
                                    21.1714137482368
                                ]
                            ]
                        ]
                    },
                    "properties": {
                        "id": 1,
                        "spatial_source": 4,
                        "user_id": "1",
                        "area": null,
                        "land_use": null,
                        "gov_pin": null,
                        "active": true,
                        "time_created": "2015-08-06T15:41:26.440037-07:00",
                        "time_updated": null,
                        "created_by": 1,
                        "updated_by": null
                    }
                }]
            }
        '''
        responses.add(responses.GET, 'http://cadasta.api/parcels',
                      body=body,
                      content_type="application/json")

        result = helpers.call_action(
            'cadasta_show_parcel',
        )

        assert_equal({
            u'features': [{
                u'geometry': {
                    u'coordinates': [[[-105.228338241577,
                                       21.1714137482368],
                                      [-105.229024887085,
                                       21.1694127979643],
                                      [-105.228338241577,
                                       21.1714137482368]]],
                    u'type': u'Polygon'},
                u'properties': {
                    u'active': True,
                    u'area': None,
                    u'created_by': 1,
                    u'gov_pin': None,
                    u'id': 1,
                    u'land_use': None,
                    u'spatial_source': 4,
                    u'time_created': u'2015-08-06T15:41:26.440037-07:00',
                    u'time_updated': None,
                    u'updated_by': None,
                    u'user_id': u'1'},
                u'type': u'Feature'
            }],
            u'type': u'FeatureCollection'},
            result)
