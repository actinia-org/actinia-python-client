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

import os

from actinia import Actinia
from actinia.vector import Vector

from .actinia_config import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    ACTINIA_AUTH,
    LOCATION_NAME,
    MAPSET_NAME,
    VECTOR_NAME,
)

NEW_MAPSET_NAME = "new_test_mapset"
UPLOAD_VECTOR_GEOJSON = "../test_data/firestations.geojson"
UPLOAD_VECTOR_NAME = "test_vector"


class TestActiniaVector(object):
    @classmethod
    def setup_class(cls):
        cls.testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication(ACTINIA_AUTH[0], ACTINIA_AUTH[1])
        cls.testactinia.get_locations()
        cls.testactinia.locations[LOCATION_NAME].get_mapsets()
        cls.testactinia.locations[LOCATION_NAME].create_mapset(NEW_MAPSET_NAME)

    @classmethod
    def teardown_class(cls):
        if NEW_MAPSET_NAME in cls.testactinia.locations[LOCATION_NAME].mapsets:
            cls.testactinia.locations[LOCATION_NAME].delete_mapset(
                NEW_MAPSET_NAME
            )

    def test_get_vectors_and_vector_info(self):
        """Test get_vector_layers and get_info methods."""
        # get vector layers
        resp = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .get_vector_layers()
        )
        assert isinstance(resp, dict), "response is not a dictionary"
        assert VECTOR_NAME in resp, f"'{VECTOR_NAME}' vector not in response"
        assert isinstance(
            resp[VECTOR_NAME], Vector
        ), "Vector not of type Vector"
        assert (
            resp
            == self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .vector_layers
        )

        # get vector info
        resp = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .vector_layers[VECTOR_NAME]
            .get_info()
        )

        vector = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .vector_layers[VECTOR_NAME]
        )
        assert isinstance(resp, dict), "response is not a dictionary"
        assert "Attributes" in resp, "response is not correct"
        assert len(resp["Attributes"]) == 25, "response is not correct"
        assert resp["north"] == "318097.688745074", "response is not correct"
        assert resp["boundaries"] == "1910", "response is not correct"
        # assert vector_info_resp == resp, "response is not correct"
        assert vector.info == resp, "vector info is not set correctly"
        assert vector.region is not None, "vector region is not set"

    def test_upload_and_delete_vector(self):
        """Test upload_vector and delete_vector methods."""
        #  upload
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tif_path = os.path.join(dir_path, UPLOAD_VECTOR_GEOJSON)
        self.testactinia.locations[LOCATION_NAME].mapsets[
            NEW_MAPSET_NAME
        ].upload_vector(UPLOAD_VECTOR_NAME, tif_path)
        vector_layers = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .vector_layers
        )
        assert UPLOAD_VECTOR_NAME in vector_layers

        # delete
        self.testactinia.locations[LOCATION_NAME].mapsets[
            NEW_MAPSET_NAME
        ].delete_vector(UPLOAD_VECTOR_NAME)
        vector_layers = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .vector_layers
        )
        assert UPLOAD_VECTOR_NAME not in vector_layers
