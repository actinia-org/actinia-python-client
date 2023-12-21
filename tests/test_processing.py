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
from actinia.job import Job

from .actinia_config import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    ACTINIA_AUTH,
    LOCATION_NAME,
)

NEW_MAPSET_NAME = "new_test_mapset"
PC = {
    "list": [
        {
            "id": "r_mapcalc",
            "module": "r.mapcalc",
            "inputs": [{"param": "expression", "value": "elevation=42"}],
        },
        {
            "module": "exporter",
            "id": "elevation_export",
            "outputs": [
                {
                    "param": "map",
                    "value": "elevation",
                    "export": {"format": "GTiff", "type": "raster"},
                }
            ],
        },
    ],
    "version": "1",
}


class TestActiniaProcessing(object):
    @classmethod
    def setup_class(cls):
        cls.testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication(ACTINIA_AUTH[0], ACTINIA_AUTH[1])
        cls.testactinia.get_locations()
        cls.testactinia.locations[LOCATION_NAME].create_mapset(NEW_MAPSET_NAME)

    @classmethod
    def teardown_class(cls):
        if NEW_MAPSET_NAME in cls.testactinia.locations[LOCATION_NAME].mapsets:
            cls.testactinia.locations[LOCATION_NAME].delete_mapset(
                NEW_MAPSET_NAME
            )

    def test_async_ephemeral_processing(self):
        """Test async ephemeral processing."""
        job = self.testactinia.locations[
            LOCATION_NAME
        ].create_processing_export_job(PC)
        assert isinstance(job, Job), "No job returned!"
        # poll job
        job.poll_until_finished()
        assert job.status == "finished", "Job status not 'finished'!"
        # check export url
        assert job.urls["resources"][0].endswith("elevation.tif")

    def test_async_persistent_processing(self):
        """Test async persistent processing."""
        job = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .create_processing_job(PC)
        )
        assert isinstance(job, Job), "No job returned!"
        # poll job
        job.poll_until_finished()
        assert job.status == "finished", "Job status not 'finished'!"
        # check created raster
        rasters = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .get_raster_layers()
        )
        assert "elevation" in rasters
