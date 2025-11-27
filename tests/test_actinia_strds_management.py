#!/usr/bin/env python
"""Test cases for actinia STRDS management.

actinia-python-client is a python client for actinia - an open source REST
API for scalable, distributed, high performance processing of geographical
data that uses GRASS GIS for computational tasks.

Copyright (c) 2023 mundialis GmbH & Co. KG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann, Stefan Bøumentrath"
__copyright__ = "Copyright 2023-2024, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

from pathlib import Path

from actinia import Actinia
from actinia.strds import SpaceTimeRasterDataset

from .actinia_config import (
    ACTINIA_AUTH,
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    LOCATION_NAME,
    STRDS_NAME,
)

NEW_MAPSET_NAME = "new_test_mapset"
UPLOAD_RASTER_TIF = "../test_data/elevation.tif"
UPLOAD_RASTER_NAME = "test_raster"
STRDS_INFO_KEYS = {
    "aggregation_type",
    "bottom",
    "creation_time",
    "creator",
    "east",
    "end_time",
    "ewres_max",
    "ewres_min",
    "granularity",
    "id",
    "map_time",
    "mapset",
    "max_max",
    "max_min",
    "min_max",
    "min_min",
    "modification_time",
    "name",
    "north",
    "nsres_max",
    "nsres_min",
    "number_of_maps",
    "number_of_semantic_labels",
    "raster_register",
    "semantic_labels",
    "semantic_type",
    "south",
    "start_time",
    "temporal_type",
    "top",
    "west",
}


class TestActiniaSpaceTimeRasterDatasets:
    """Test SpaceTimeRasterDatasets management."""

    @classmethod
    def setup_class(cls) -> None:
        """Set up test environment."""
        cls.testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication(ACTINIA_AUTH[0], ACTINIA_AUTH[1])
        cls.testactinia.get_locations()
        cls.testactinia.locations[LOCATION_NAME].get_mapsets()
        cls.testactinia.locations[LOCATION_NAME].create_mapset(NEW_MAPSET_NAME)

    @classmethod
    def teardown_class(cls) -> None:
        """Tear down test environment."""
        if NEW_MAPSET_NAME in cls.testactinia.locations[LOCATION_NAME].mapsets:
            cls.testactinia.locations[LOCATION_NAME].delete_mapset(
                NEW_MAPSET_NAME,
            )

    def test_get_strds_info(self) -> None:
        """Test STRDS management."""
        # Create STRDS
        resp = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .create_strds(
                STRDS_NAME,
                "test title",
                "test description",
                "absolute",
            )
        )
        strds = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .strds
        )
        assert isinstance(strds, dict), "response is not a dictionary"
        assert STRDS_NAME in strds, f"STRDS '{STRDS_NAME}' is not in response"
        assert isinstance(
            strds[STRDS_NAME],
            SpaceTimeRasterDataset,
        ), "STRDS is not of type SpaceTimeRasterDataset"

        # Get STRDS info
        resp = strds[STRDS_NAME].get_info()
        key_difference = STRDS_INFO_KEYS.difference(set(resp.keys()))
        assert isinstance(resp, dict), "response is not a dictionary"
        assert not key_difference, f"keys {key_difference} missing in response"

        # Get STRDS raster layers from empty STRDS
        # do not fail, but report empty STRDS / selection
        resp = strds[STRDS_NAME].get_strds_raster_layers()
        assert isinstance(resp, list), "response is not a list"

        # Register raster to STRDS and check registration
        dir_path = Path(__file__).resolve().parent
        tif_path = (dir_path / UPLOAD_RASTER_TIF).resolve()
        self.testactinia.locations[LOCATION_NAME].mapsets[
            NEW_MAPSET_NAME
        ].upload_raster(UPLOAD_RASTER_NAME, str(tif_path))
        strds[STRDS_NAME].register_raster_layer(
            UPLOAD_RASTER_NAME,
            "2023-01-01 00:00:00",
        )
        resp = strds[STRDS_NAME].get_strds_raster_layers()
        assert isinstance(resp, list), "response is not a list"

        # Test unregistering raster from STRDS
        strds[STRDS_NAME].unregister_raster_layer([UPLOAD_RASTER_NAME])

        # Delete STRDS
        resp = (
            self.testactinia.locations[LOCATION_NAME]
            .mapsets[NEW_MAPSET_NAME]
            .delete_strds(STRDS_NAME)
        )
