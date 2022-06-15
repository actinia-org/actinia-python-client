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
import requests

from actinia.raster import Raster
from actinia.utils import request_and_check, print_stdout
from actinia.job import Job


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

    def get_raster_layers(self, force=False):
        """
        Return raster layers
        """
        if self.raster_layers is None or force is True:
            self.__request_raster_layers()
        return self.raster_layers

    def upload_raster(self, layer_name, tif_file):
        """Upload GTiff as a raster layer
        Parameters:
            layername (string): Name for the raster layer
            tif_file (string): Path of the GTiff file to upload
        """
        files = {"file": (tif_file, open(tif_file, "rb"))}
        url = f"{self.__actinia.url}/locations/{self.__location_name}/" \
            f"mapsets/{self.name}/raster_layers/{layer_name}"
        resp = requests.post(
                url=url,
                files=files,
                auth=self.__auth,
        )
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        kwargs = json.loads(resp.text)
        job = Job(
            f"raster_upload_{self.__location_name}_{self.name}_{layer_name}",
            self.__actinia, self.__auth, **kwargs)
        job.poll_until_finished()
        if job.status != "finished":
            raise Exception(f"{job.status}: {job.message}")
        if self.raster_layers is None:
            self.get_raster_layers()
        self.raster_layers[layer_name] = Raster(
            layer_name, self.__location_name, self.name,
            self.__actinia, self.__auth
        )

    def delete_raster(self, layer_name):
        """Delete a raster layer"""
        url = f"{self.__actinia.url}/locations/{self.__location_name}/" \
            f"mapsets/{self.name}/raster_layers/{layer_name}"
        resp = requests.delete(
                url=url,
                auth=self.__auth,
        )
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        if self.raster_layers is None:
            self.get_raster_layers()
        else:
            del self.raster_layers[layer_name]
        print_stdout(f"Raster <{layer_name}> successfully deleted")

# TODO:
# * /locations/{location_name}/mapsets/{mapset_name} - DELETE, POST
# * /locations/{location_name}/mapsets/{mapset_name}/info - GET
# * (/locations/{location_name}/mapsets/{mapset_name}/lock - GET, DELETE, POST)

# * /locations/{location_name}/mapsets/{mapset_name}/raster_layers
#      - DELETE, PUT
# * /locations/{location_name}/mapsets/{mapset_name}/strds - GET
# * "/locations/{location_name}/mapsets/{mapset_name}/vector_layers"

# * (/locations/{location_name}/mapsets/{mapset_name}/processing
#          - POST (persistent, asyncron))
# * /locations/{location_name}/mapsets/{mapset_name}/processing_async
#          - POST (persistent, asyncron)
