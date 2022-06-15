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
import os
from unittest.mock import Mock, patch

from actinia import Actinia
from actinia.raster import Raster

from .mock.actinia_mock import (
    ACTINIA_BASEURL,
    version_resp_text,
    location_get_mapset_resp,
)
from .mock.actinia_location_management_mock import get_locations_resp
from .mock.actinia_raster_management_mock import (
    get_rasters_mock,
    get_raster_info_mock,
    raster_info_resp,
    upload_raster_resp,
    delete_raster_resp,
    start_job_resp,
)


LOCATION_NAME = "nc_spm_08"
MAPSET_NAME = "PERMANENT"
RASTER_NAME = "zipcodes"
UPLOAD_RASTER_TIF = "./data/elevation.tif"
UPLOAD_RASTER_NAME = "test_raster"


class TestActiniaRaster(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch("actinia.actinia.requests.get")
        cls.mock_post_patcher = patch("actinia.actinia.requests.post")
        cls.mock_delete_patcher = patch("actinia.actinia.requests.delete")
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_post = cls.mock_post_patcher.start()
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
        # get mapsets
        cls.mock_get.return_value = Mock()
        cls.mock_get.return_value.status_code = 200
        cls.mock_get.return_value.text = json.dumps(location_get_mapset_resp)
        cls.testactinia.locations[LOCATION_NAME].get_mapsets()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()
        cls.mock_delete_patcher.stop()

    def test_get_rasters_and_raster_info(self):
        """Test get_raster_layers and get_info methods."""
        # get raster layers
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(get_rasters_mock)
        resp = self.testactinia.locations[LOCATION_NAME].mapsets[
            MAPSET_NAME].get_raster_layers()

        assert isinstance(resp, dict), "response is not a dictionary"
        assert "zipcodes" in resp, "'zipcodes' raster not in response"
        assert isinstance(
            resp["zipcodes"], Raster
        ), "Rasters not of type Raster"
        assert resp == self.testactinia.locations[LOCATION_NAME].mapsets[
            MAPSET_NAME].raster_layers

        # get raster info
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(get_raster_info_mock)
        resp = self.testactinia.locations[LOCATION_NAME].mapsets[
            MAPSET_NAME].raster_layers[RASTER_NAME].get_info()

        raster = self.testactinia.locations[LOCATION_NAME].mapsets[
            MAPSET_NAME].raster_layers[RASTER_NAME]
        assert isinstance(resp, dict), "response is not a dictionary"
        assert raster_info_resp == resp, "response is not correct"
        assert raster.info == resp, "raster info is not set correctly"
        assert raster.region is not None, "raster region is not set"

    def test_upload_and_delete_raster(self):
        """Test upload_raster and delete_raster methods."""
        # mockup
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(upload_raster_resp)
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.text = json.dumps(start_job_resp)
        self.mock_delete.return_value = Mock()
        self.mock_delete.return_value.status_code = 200
        self.mock_delete.return_value.text = json.dumps(delete_raster_resp)

        #  upload
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tif_path = os.path.join(dir_path, UPLOAD_RASTER_TIF)
        self.testactinia.locations[LOCATION_NAME].mapsets[
            MAPSET_NAME].upload_raster(UPLOAD_RASTER_NAME, tif_path)
        raster_layers = self.testactinia.locations[LOCATION_NAME].mapsets[
            MAPSET_NAME].raster_layers
        assert UPLOAD_RASTER_NAME in raster_layers

        # delete
        self.testactinia.locations[LOCATION_NAME].mapsets[
            MAPSET_NAME].delete_raster(UPLOAD_RASTER_NAME)
        raster_layers = self.testactinia.locations[LOCATION_NAME].mapsets[
            MAPSET_NAME].raster_layers
        assert UPLOAD_RASTER_NAME not in raster_layers
