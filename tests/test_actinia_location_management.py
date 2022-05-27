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
from actinia.location import Location
from actinia.region import Region


from .mock.actinia_mock import (
    ACTINIA_BASEURL,
    version_resp_text,
)

from .mock.actinia_location_management_mock import (
    location_creation_resp,
    get_locations_resp,
    delete_location_resp,
    location_get_info_resp,
)

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"

LOCATION_NAME = "nc_spm_08"
NEW_LOCATION_NAME = "test_location"
EPSGCODE = 25832


class TestActinia(object):
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

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()
        cls.mock_delete_patcher.stop()
        if NEW_LOCATION_NAME in cls.testactinia.locations:
            cls.mock_delete_location()
            cls.testactinia.locations[NEW_LOCATION_NAME].delete()

    @classmethod
    def mock_delete_location(cls):
        cls.mock_delete.return_value = Mock()
        cls.mock_delete.return_value.status_code = 200
        cls.mock_delete.return_value.text = json.dumps(delete_location_resp)

    def test_actinia_get_locations(self):
        """Test get locations."""

        assert self.testactinia.locations == {}, (
            "Locations are not empty dictionary"
        )

        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(get_locations_resp)

        locations = self.testactinia.get_locations()
        assert "nc_spm_08" in locations, "'nc_spm_08' not in locations"
        assert isinstance(locations, dict), "locations not of type dictionary"
        assert isinstance(
            locations["nc_spm_08"], Location
        ), "location not of type Location"
        assert (
            locations["nc_spm_08"].name == "nc_spm_08"
        ), "location.name is wrong"
        assert self.testactinia.locations == locations

    def test_location_get_info(self):
        """Test location get_info method."""
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(location_get_info_resp)
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
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.text = json.dumps(location_creation_resp)

        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(get_locations_resp)

        # create location
        location = self.testactinia.create_location(
            NEW_LOCATION_NAME, EPSGCODE)
        assert isinstance(location, Location), \
            "Created location is not of type Location"
        assert location.name == NEW_LOCATION_NAME, \
            "Created location name is wrong"
        assert NEW_LOCATION_NAME in self.testactinia.locations, \
            "Created location is not added to locations"

        # Delete location
        self.mock_delete_location()
        self.testactinia.locations[NEW_LOCATION_NAME].delete()
        assert NEW_LOCATION_NAME not in self.testactinia.locations, \
            "Location not deleted"
