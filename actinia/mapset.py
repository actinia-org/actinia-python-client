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

from actinia.raster import Raster
from actinia.utils import request_and_check


class Mapset:
    def __init__(self, name, location_name, actinia, auth):
        self.name = name
        self.projection = None
        self.region = None
        self.__location_name = location_name
        self.__actinia = actinia
        self.__auth = auth
        self.raster_layers = None
        self.vector_layers = None
        self.strds = None

    def __request_raster_layers(self):
        """
        Requests the raster layers in the mapset.

        :return: A list of the mapset names
        """
        url = f"{self.__actinia.url}/locations/{self.__location_name}/" \
            f"mapsets/{self.name}/raster_layers"
        resp = request_and_check(url, auth=self.__auth)
        raster_names = resp["process_results"]
        rasters = {
            mname: Raster(
                mname, self.__location_name, self.name,
                self.__actinia, self.__auth
            )
            for mname in raster_names
        }
        self.raster_layers = rasters

    def get_raster_layers(self):
        """
        Return raster layers
        """
        if self.raster_layers is None:
            self.__request_raster_layers()
        return self.raster_layers

    # def create_raster_layer(self, name, file):
    #     """
    #     Creates a raster layer from a given GTif file
    #     """
    #     url = f"{self.__actinia.url}/locations/{self.__location_name}/" \
    #         f"mapsets/{self.name}/raster_layers/{name}"
    #     # TODO
    #     # import pdb; pdb.set_trace()


# TODO:
# * /locations/{location_name}/mapsets/{mapset_name} - DELETE, POST
# * /locations/{location_name}/mapsets/{mapset_name}/info - GET
# * (/locations/{location_name}/mapsets/{mapset_name}/lock - GET, DELETE, POST)

# * /locations/{location_name}/mapsets/{mapset_name}/raster_layers
#      - DELETE, GET, PUT
# * /locations/{location_name}/mapsets/{mapset_name}/strds - GET
# * "/locations/{location_name}/mapsets/{mapset_name}/vector_layers"

# * (/locations/{location_name}/mapsets/{mapset_name}/processing
#          - POST (persistent, asyncron))
# * /locations/{location_name}/mapsets/{mapset_name}/processing_async
#          - POST (persistent, asyncron)
