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


class TestParcelDetail(object):
    def teardown(self):
        helpers.reset_db()
        search.clear_all()

    @responses.activate
    def test_get_one(self):
        body = ''' {
            "type": "FeatureCollection",
            "features": [
                {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                    -73.724739,
                    40.588342
                    ]
                },
                "properties": {
                    "id": 1,
                    "spatial_source": 1,
                    "user_id": "11",
                    "area": null,
                    "land_use": null,
                    "gov_pin": null,
                    "active": true,
                    "sys_delete": false,
                    "time_created": "2015-09-01T09:53:16.466337-07:00",
                    "time_updated": null,
                    "created_by": 11,
                    "updated_by": null,
                    "parcel_history": [
                    {
                        "id": 1,
                        "parcel_id": 1,
                        "origin_id": 1,
                        "parent_id": null,
                        "version": 1,
                        "description": "new description",
                        "date_modified": "2015-09-01T07:00:00.000Z",
                        "active": true,
                        "time_created": "2015-09-01T16:53:16.466Z",
                        "time_updated": null,
                        "created_by": 11,
                        "updated_by": null
                    }
                    ],
                    "relationships": [
                    {
                        "id": 1,
                        "parcel_id": 1,
                        "party_id": 1,
                        "geom_id": null,
                        "tenure_type": 1,
                        "acquired_date": null,
                        "how_acquired": null,
                        "active": true,
                        "sys_delete": false,
                        "time_created": "2015-09-01T16:53:16.466Z",
                        "time_updated": null,
                        "created_by": 11,
                        "updated_by": null
                    }
                    ]
                }
                }
            ]
            }
        '''
        responses.add(responses.GET, 'http://cadasta.api/parcels/1/details',
                      body=body,
                      content_type="application/json")

        result = helpers.call_action(
            'cadasta_show_parcel_detail',
            id=1,
            project_id=1,
        )

        assert_equal({
            u'features': [{
                u'geometry': {
                    u'coordinates': [-73.724739, 40.588342],
                    u'type': u'Point'
                },
                u'properties': {
                    u'active': True,
                    u'area': None,
                    u'created_by': 11,
                    u'gov_pin': None,
                    u'id': 1,
                    u'land_use': None,
                    u'parcel_history': [{
                        u'active': True,
                        u'created_by': 11,
                        u'date_modified': u'2015-09-01T07:00:00.000Z',
                        u'description': u'new description',
                        u'id': 1,
                        u'origin_id': 1,
                        u'parcel_id': 1,
                        u'parent_id': None,
                        u'time_created': u'2015-09-01T16:53:16.466Z',
                        u'time_updated': None,
                        u'updated_by': None,
                        u'version': 1}
                    ],
                    u'relationships': [{
                        u'acquired_date': None,
                        u'active': True,
                        u'created_by': 11,
                        u'geom_id': None,
                        u'how_acquired': None,
                        u'id': 1,
                        u'parcel_id': 1,
                        u'party_id': 1,
                        u'sys_delete': False,
                        u'tenure_type': 1,
                        u'time_created': u'2015-09-01T16:53:16.466Z',
                        u'time_updated': None,
                        u'updated_by': None}],
                    u'spatial_source': 1,
                    u'sys_delete': False,
                    u'time_created': u'2015-09-01T09:53:16.466337-07:00',
                    u'time_updated': None,
                    u'updated_by': None,
                    u'user_id': u'11'},
                u'type': u'Feature'}],
            u'type': u'FeatureCollection'},
            result
        )
