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

from actinia.region import Region
from actinia.utils import request_and_check, print_stdout


class STRDS:
    def __init__(self, name, location_name, mapset_name, actinia, auth):
        self.name = name
        self.__location_name = location_name
        self.__mapset_name = mapset_name
        self.__actinia = actinia
        self.__auth = auth
        self.region = None
        self.info = None
        self.start_time = None
        self.end_time = None
        self.granularity = None
        self.raster_layers = None

    def get_info(self, force=False):
        """Return the informations of the STRDS map
        """
        if self.info is None or force is True:
            url = f"{self.__actinia.url}/locations/{self.__location_name}/" \
                f"mapsets/{self.__mapset_name}/strds/{self.name}"
            resp = request_and_check(url, self.__auth)
            info = resp["process_results"]
            self.info = info

            self.start_time = info["start_time"]
            self.end_time = info["end_time"]
            self.granularity = info["granularity"]

            self.region = Region(
                zone=None,
                projection=None,
                n=info["north"],
                s=info["south"],
                e=info["east"],
                w=info["west"],
                t=info["top"],
                b=info["bottom"],
                nsres=None,
                ewres=None,
                nsres3=None,
                ewres3=None,
                tbres=None,
                rows=None,
                cols=None,
                rows3=None,
                cols3=None,
                depths=None,
                cells=None,
                cells3=None
            )
        print_stdout(json.dumps(self.info, indent=4))
        return self.info

    def get_raster_layers(self, force=False):
        """Return the informations of the STRDS map
        """
        if self.raster_layers is None or force is True:
            url = f"{self.__actinia.url}/locations/{self.__location_name}/" \
                f"mapsets/{self.__mapset_name}/strds/{self.name}/raster_layers"
            resp = request_and_check(url, self.__auth)
            # import pdb; pdb.set_trace()
            rasters = resp["process_results"]
            self.raster_layers = dict()
            for rast in rasters:
                name, mapset = rast["id"].split("@")
                rast["name"] = name
                rast["mapset"] = mapset
                self.raster_layers[rast["id"]] = rast
        return self.raster_layers

    def add_raster_layers(self, raster_layers, start_times, end_times):
        """Register raster map layers in a STRDS"""

        url = f"{self.__actinia.url}/locations/{self.__location_name}/" \
            f"mapsets/{self.__mapset_name}/strds/{self.name}/raster_layers"

        kwargs = dict()
        kwargs["headers"] = self.__actinia.headers
        kwargs["auth"] = self.__auth
        name = raster_layers
        start_time = start_times
        end_time = end_times
        data = list()
        for name, start_time, end_time in zip(
                raster_layers.split(","), start_times.split(","),
                end_times.split(",")):
            data.append({
                "name": name,
                "start_time": start_time,
                "end_time": end_time,
            })
        kwargs["data"] = json.dumps(data)
        try:
            resp = requests.put(url, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise e
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        self.get_raster_layers(force=True)
        print_stdout(f"Raster maps <{raster_layers}> added to STRDS.")

    def remove_raster_layers(self, raster_layers):
        """Register raster map layers in a STRDS"""

        url = f"{self.__actinia.url}/locations/{self.__location_name}/" \
            f"mapsets/{self.__mapset_name}/strds/{self.name}/raster_layers"

        kwargs = dict()
        kwargs["headers"] = self.__actinia.headers
        kwargs["auth"] = self.__auth
        kwargs["data"] = json.dumps(raster_layers.split(","))
        try:
            resp = requests.delete(url, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise e
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        self.get_raster_layers(force=True)
        print_stdout(f"Raster maps <{raster_layers}> removed from STRDS.")


# TODO:
# * /locations/{location_name}/mapsets/{mapset_name}/strds/{strds_name}/
#           render - GET
