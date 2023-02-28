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
from actinia.location import Location
from actinia.region import Region

from .actinia_config import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    ACTINIA_AUTH,
    LOCATION_NAME,
)

NEW_LOCATION_NAME = "test_location"
EPSGCODE = 25832


class TestActinia(object):
    @classmethod
    def setup_class(cls):
        cls.testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication(ACTINIA_AUTH[0], ACTINIA_AUTH[1])

    @classmethod
    def teardown_class(cls):
        if NEW_LOCATION_NAME in cls.testactinia.locations:
            cls.testactinia.locations[NEW_LOCATION_NAME].delete()

    def test_actinia_get_locations(self):
        """Test get locations."""

        assert (
            self.testactinia.locations == {}
        ), "Locations may not be an empty dictionary"

        locations = self.testactinia.get_locations()
        assert (
            LOCATION_NAME in locations
        ), f"'{LOCATION_NAME}' not in locations"
        assert isinstance(locations, dict), "locations not of type dictionary"
        assert isinstance(
            locations[LOCATION_NAME], Location
        ), "location not of type Location"
        assert (
            locations[LOCATION_NAME].name == LOCATION_NAME
        ), "location.name is wrong"
        assert self.testactinia.locations == locations

    def test_location_get_info(self):
        """Test location get_info method."""

        resp = self.testactinia.locations[LOCATION_NAME].get_info()

        assert "region" in resp, "'region' not in location info"
        assert "projection" in resp, "'projection' not in location info"
        assert isinstance(resp["projection"], str), "'projection' wrong type"
        assert isinstance(resp["region"], Region), "'region' wrong type"
        region = resp["region"]
        assert hasattr(region, "n"), "Region has not the attribute 'n'"
        assert region == self.testactinia.locations[LOCATION_NAME].region
        assert (
            resp["projection"]
            == self.testactinia.locations[LOCATION_NAME].projection
        )

    def test_actinia_create_and_delete_locations(self):
        """Test location creation and deletion"""

        # create location
        location = self.testactinia.create_location(
            NEW_LOCATION_NAME, EPSGCODE
        )
        assert isinstance(
            location, Location
        ), "Created location is not of type Location"
        assert (
            location.name == NEW_LOCATION_NAME
        ), "Created location name is wrong"
        assert (
            NEW_LOCATION_NAME in self.testactinia.locations
        ), "Created location is not added to locations"

        # Delete location
        self.testactinia.locations[NEW_LOCATION_NAME].delete()
        assert (
            NEW_LOCATION_NAME not in self.testactinia.locations
        ), "Location not deleted"
