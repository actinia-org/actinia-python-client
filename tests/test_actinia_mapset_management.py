#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# Copyright (c) 2023 mundialis GmbH & Co. KG
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
__copyright__ = "Copyright 2023, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

from actinia import Actinia
from actinia.mapset import Mapset
from actinia.region import Region

from .actinia_config import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    ACTINIA_AUTH,
    LOCATION_NAME,
    MAPSET_NAME,
)

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
        cls.testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication(ACTINIA_AUTH[0], ACTINIA_AUTH[1])
        cls.testactinia.get_locations()

    @classmethod
    def teardown_class(cls):
        if NEW_MAPSET_NAME in cls.testactinia.locations[LOCATION_NAME].mapsets:
            cls.testactinia.locations[LOCATION_NAME].delete_mapset(
                NEW_MAPSET_NAME
            )

    def test_location_get_mapsets(self):
        """Test location get_mapsets method."""
        resp = self.testactinia.locations[LOCATION_NAME].get_mapsets()
        assert isinstance(resp, dict), "response is not a dictionary"
        assert "PERMANENT" in resp, "'PERMANENT' mapset not in response"
        assert isinstance(
            resp["PERMANENT"], Mapset
        ), "Mapsets not of type Mapset"
        assert resp == self.testactinia.locations[LOCATION_NAME].mapsets

    def test_mapset_get_info(self):
        """Test mapset get_info method."""
        resp = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .info()
        )
        assert "region" in resp, "'region' not in location info"
        assert "projection" in resp, "'projection' not in location info"
        assert isinstance(resp["projection"], str), "'projection' wrong type"
        assert isinstance(resp["region"], Region), "'region' wrong type"
        region = resp["region"]
        assert hasattr(region, "n"), "Region has not the attribute 'n'"
        assert (
            region
            == self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .region
        )
        assert (
            resp["projection"]
            == self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .projection
        )

    def test_actinia_create_and_delete_mapsets(self):
        """Test location creation and deletion"""
        # create mapset
        mapset = self.testactinia.locations[LOCATION_NAME].create_mapset(
            NEW_MAPSET_NAME
        )
        assert isinstance(
            mapset, Mapset
        ), "Created mapset is not of type Mapset"
        assert mapset.name == NEW_MAPSET_NAME, "Created location name is wrong"
        assert (
            NEW_MAPSET_NAME
            in self.testactinia.locations[LOCATION_NAME].mapsets
        ), "Created mapset is not added to location's mapsets"

        # Delete mapset with Location method
        self.testactinia.locations[LOCATION_NAME].delete_mapset(
            NEW_MAPSET_NAME
        )
        assert (
            NEW_MAPSET_NAME
            not in self.testactinia.locations[LOCATION_NAME].mapsets
        ), "Mapset not deleted"

        # Recreate mapset and delete with Mapset method
        mapset = self.testactinia.locations[LOCATION_NAME].create_mapset(
            NEW_MAPSET_NAME
        )
        mapset.delete()
        assert (
            NEW_MAPSET_NAME
            not in self.testactinia.locations[LOCATION_NAME].mapsets
        ), "Mapset not deleted"
