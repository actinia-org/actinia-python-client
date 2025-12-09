#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# SPDX-FileCopyrightText: (c) 2023 mundialis GmbH & Co. KG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#######

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2023, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import os

from actinia import Actinia
from actinia.raster import Raster

from .actinia_config import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    ACTINIA_AUTH,
    LOCATION_NAME,
    MAPSET_NAME,
    RASTER_NAME,
)

NEW_MAPSET_NAME = "new_test_mapset"
UPLOAD_RASTER_TIF = "../test_data/elevation.tif"
UPLOAD_RASTER_NAME = "test_raster"


class TestActiniaRaster(object):
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

    def test_get_rasters_and_raster_info(self):
        """Test get_raster_layers and get_info methods."""
        # get raster layers
        resp = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .get_raster_layers()
        )

        assert isinstance(resp, dict), "response is not a dictionary"
        assert RASTER_NAME in resp, f"'{RASTER_NAME}' raster not in response"
        assert isinstance(
            resp[RASTER_NAME], Raster
        ), "Rasters not of type Raster"
        assert (
            resp
            == self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .raster_layers
        )

        # get raster info
        resp = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .raster_layers[RASTER_NAME]
            .get_info()
        )

        raster = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[MAPSET_NAME]
            .raster_layers[RASTER_NAME]
        )
        assert isinstance(resp, dict), "response is not a dictionary"
        assert "cells" in resp, "response is not correct"
        assert resp["cells"] == "2025000", "response is not correct"
        assert resp["min"] == "55.57879", "response is not correct"
        assert raster.info == resp, "raster info is not set correctly"
        assert raster.region is not None, "raster region is not set"

    def test_upload_and_delete_raster(self):
        """Test upload_raster and delete_raster methods."""
        #  upload
        dir_path = os.path.dirname(os.path.realpath(__file__))
        tif_path = os.path.join(dir_path, UPLOAD_RASTER_TIF)
        self.testactinia.locations[LOCATION_NAME].mapsets[
            NEW_MAPSET_NAME
        ].upload_raster(UPLOAD_RASTER_NAME, tif_path)
        raster_layers = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .raster_layers
        )
        assert UPLOAD_RASTER_NAME in raster_layers

        # delete uploaded raster
        self.testactinia.locations[LOCATION_NAME].mapsets[
            NEW_MAPSET_NAME
        ].delete_raster(UPLOAD_RASTER_NAME)
        raster_layers = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .raster_layers
        )
        assert UPLOAD_RASTER_NAME not in raster_layers
