#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# Copyright (c) 2022 mundialis GmbH & Co. KG
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
#######

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import json
from unittest.mock import Mock, patch

from actinia import Actinia
from actinia.mapset import Mapset
from actinia.region import Region

from .mock.actinia_mock import (
    ACTINIA_BASEURL,
    ACTINIA_TEST_AUTH,
    ACTINIA_API_PREFIX,
    version_resp_text,
    location_get_mapset_resp,
)

from .mock.actinia_location_management_mock import get_locations_resp

from .mock.actinia_mapset_management_mock import (
    mapset_get_info_resp,
    mapset_creation_resp,
    delete_mapset_resp
)

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"

LOCATION_NAME = "nc_spm_08"
NEW_LOCATION_NAME = "test_location"
EPSGCODE = 25832
MAPSET_NAME = "test_mapset"
NEW_MAPSET_NAME = "new_test_mapset"
PC = {
    "list": [
        {
            "id": "r_mapcalc",
            "module": "r.mapcalc",
            "inputs": [{"param": "expression", "value": "elevation=42"}],
        }
    ],
    "version": "1",
}


class TestActiniaLocation(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch("actinia.actinia.requests.get")
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_post_patcher = patch("actinia.actinia.requests.post")
        cls.mock_post = cls.mock_post_patcher.start()
        cls.mock_delete_patcher = patch("actinia.actinia.requests.delete")
        cls.mock_delete = cls.mock_delete_patcher.start()

        cls.mock_get.return_value = Mock()
        cls.mock_get.return_value.status_code = 200
        cls.mock_get.return_value.text = json.dumps(version_resp_text)
        cls.testactinia = Actinia(ACTINIA_BASEURL)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication("user", "pw")
        # get locations
        cls.mock_get.return_value = Mock()
        cls.mock_get.return_value.status_code = 200
        cls.mock_get.return_value.text = json.dumps(get_locations_resp)
        cls.testactinia.get_locations()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()
        cls.mock_delete_patcher.stop()
        if NEW_LOCATION_NAME in cls.testactinia.locations:
            cls.mock_delete_mapset()
            cls.testactinia.locations[NEW_LOCATION_NAME].delete_mapset(
                NEW_MAPSET_NAME
            )

    @classmethod
    def mock_delete_mapset(cls):
        cls.mock_delete.return_value = Mock()
        cls.mock_delete.return_value.status_code = 200
        cls.mock_delete.return_value.text = json.dumps(delete_mapset_resp)

    def test_location_get_mapsets(self):
        """Test location get_mapsets method."""
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(location_get_mapset_resp)
        resp = self.testactinia.locations[LOCATION_NAME].get_mapsets()
        self.mock_get.assert_called_with(
            f"{ACTINIA_BASEURL}/{ACTINIA_API_PREFIX}" +
            f"/locations/{LOCATION_NAME}/mapsets",
            auth=ACTINIA_TEST_AUTH
        )
        assert isinstance(resp, dict), "response is not a dictionary"
        assert "PERMANENT" in resp, "'PERMANENT' mapset not in response"
        assert isinstance(
            resp["PERMANENT"], Mapset
        ), "Mapsets not of type Mapset"
        assert resp == self.testactinia.locations[LOCATION_NAME].mapsets

    def test_mapset_get_info(self):
        """Test mapset get_info method."""
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(mapset_get_info_resp)
        resp = self.testactinia.locations[
            LOCATION_NAME
        ].mapsets[MAPSET_NAME].info()

        self.mock_get.assert_called_with(
            f"{ACTINIA_BASEURL}/{ACTINIA_API_PREFIX}" +
            f"/locations/{LOCATION_NAME}" +
            f"/mapsets/{MAPSET_NAME}/info",
            auth=ACTINIA_TEST_AUTH
        )
        assert "region" in resp, "'region' not in location info"
        assert "projection" in resp, "'projection' not in location info"
        assert isinstance(resp["projection"], str), "'projection' wrong type"
        assert isinstance(resp["region"], Region), "'region' wrong type"
        region = resp["region"]
        assert hasattr(region, "n"), "Region has not the attribute 'n'"
        assert region == self.testactinia.locations[
            LOCATION_NAME
        ].mapsets[MAPSET_NAME].region
        assert (
            resp["projection"]
            == self.testactinia.locations[
                LOCATION_NAME
            ].mapsets[MAPSET_NAME].projection
        )

    def test_actinia_create_and_delete_mapsets(self):
        """Test location creation and deletion"""
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.text = json.dumps(mapset_creation_resp)

        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(location_get_mapset_resp)

        # create mapset
        mapset = self.testactinia.locations[LOCATION_NAME].create_mapset(
            NEW_MAPSET_NAME
        )
        self.mock_post.assert_called_with(
            f"{ACTINIA_BASEURL}/{ACTINIA_API_PREFIX}" +
            f"/locations/{LOCATION_NAME}" +
            f"/mapsets/{NEW_MAPSET_NAME}",
            auth=ACTINIA_TEST_AUTH
        )
        assert isinstance(mapset, Mapset), \
            "Created mapset is not of type Mapset"
        assert mapset.name == NEW_MAPSET_NAME, \
            "Created location name is wrong"
        assert NEW_MAPSET_NAME in self.testactinia.locations[
            LOCATION_NAME
        ].mapsets, \
            "Created mapset is not added to location's mapsets"

        # Delete mapset with Location method
        self.mock_delete_mapset()
        self.testactinia.locations[LOCATION_NAME].delete_mapset(
            NEW_MAPSET_NAME
        )
        self.mock_delete.assert_called_with(
            f"{ACTINIA_BASEURL}/{ACTINIA_API_PREFIX}" +
            f"/locations/{LOCATION_NAME}" +
            f"/mapsets/{NEW_MAPSET_NAME}",
            auth=ACTINIA_TEST_AUTH
        )
        assert NEW_MAPSET_NAME not in self.testactinia.locations[
            LOCATION_NAME
        ].mapsets, \
            "Mapset not deleted"

        # Recreate mapset and delete with Mapset method
        mapset = self.testactinia.locations[LOCATION_NAME].create_mapset(
            NEW_MAPSET_NAME
        )
        self.mock_post.assert_called_with(
            f"{ACTINIA_BASEURL}/{ACTINIA_API_PREFIX}" +
            f"/locations/{LOCATION_NAME}" +
            f"/mapsets/{NEW_MAPSET_NAME}",
            auth=ACTINIA_TEST_AUTH
        )
        self.mock_delete()
        mapset.delete()
        self.mock_delete.assert_called_with(
            f"{ACTINIA_BASEURL}/{ACTINIA_API_PREFIX}" +
            f"/locations/{LOCATION_NAME}" +
            f"/mapsets/{NEW_MAPSET_NAME}",
            auth=ACTINIA_TEST_AUTH
        )
        assert NEW_MAPSET_NAME not in self.testactinia.locations[
            LOCATION_NAME
        ].mapsets, \
            "Mapset not deleted"
