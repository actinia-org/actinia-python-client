#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# acintia-python-client is a python client for actinia - an open source REST
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
    version_resp_text,
    location_get_mapset_resp,
)
from .mock.actinia_mapset_management_mock import mapset_get_info_resp
from .mock.actinia_location_management_mock import get_locations_resp

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"

LOCATION_NAME = "nc_spm_08"
MAPSET_NAME = "test_mapset"
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
        cls.mock_post_patcher = patch("actinia.actinia.requests.post")
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_post = cls.mock_post_patcher.start()

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

    def test_location_get_mapsets(self):
        """Test location get_mapsets method."""
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(location_get_mapset_resp)
        resp = self.testactinia.locations[LOCATION_NAME].get_mapsets()

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
        resp = self.testactinia.locations[LOCATION_NAME].mapsets[MAPSET_NAME].info()

        assert "region" in resp, "'region' not in location info"
        assert "projection" in resp, "'projection' not in location info"
        assert isinstance(resp["projection"], str), "'projection' wrong type"
        assert isinstance(resp["region"], Region), "'region' wrong type"
        region = resp["region"]
        assert hasattr(region, "n"), "Region has not the attribute 'n'"
        assert region == self.testactinia.locations[LOCATION_NAME].mapsets[MAPSET_NAME].region
        assert (
            resp["projection"]
            == self.testactinia.locations[LOCATION_NAME].mapsets[MAPSET_NAME].projection
        )