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

from .mock.actinia_mock import (
    ACTINIA_BASEURL,
    version_resp_text,
    get_locations_resp,
)

__author__ = "Anika Weinmann"
__copyright__ = "mundialis"
__license__ = "TODO"


class TestActinia(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch("actinia.actinia.requests.get")
        cls.mock_get = cls.mock_get_patcher.start()

        cls.mock_get.return_value = Mock()
        cls.mock_get.return_value.status_code = 200
        cls.mock_get.return_value.text = json.dumps(version_resp_text)
        cls.testactinia = Actinia(ACTINIA_BASEURL)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication("user", "pw")

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_actinia_get_locations(self):

        assert self.testactinia.locations == {}, (
            "Locations are not empty " "dictionary"
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
