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
__author__ = "Anika Weinmann and Corey White"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import json
import requests
from actinia.region import Region
from enum import Enum, unique


@unique
class MAPSET_TASK(Enum):
    INFO = "info"
    LOCK = "lock"
    RASTER_LAYER = "raster_layer"
    STRDS = "strds"
    VECTOR_LAYERS = "vector_layers"
    PROCESSING = "processing"
    PROCESSING_ASYNC = "processing_async"


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

    def __request_url(
        actinia_url,
        location_name,
        mapset_name=None,
        task=None
    ):
        """
        Provides the url to an Actinia mapset resource.

        Parameters
        ----------
        actinia_url : str
            The base url to actinia server
        location_name : str
            The GRASS location name
            route: /locations/{location_name}/mapsets
        mapset_name : str, default=None
            The mapset name
            route: /locations/{location_name}/mapsets/{mapset_name}
        task : Enum(MAPSET_TASK), default=None
            The requested task
            (info) route:
                /locations/{location_name}/mapsets/{mapset_name}/info
            (lock) route:
                /locations/{location_name}/mapsets/{mapset_name}/lock
            (raster_layers) route:
                /locations/{location_name}/mapsets/{mapset_name}/raster_layers
            (vector_layers) route:
                /locations/{location_name}/mapsets/{mapset_name}/vector_layers
            (strds) route:
                /locations/{location_name}/mapsets/{mapset_name}/strds
            (processing) route:
                /locations/{location_name}/mapsets/{mapset_name}/processing
            (processing_async) route:
                /locations/{location_name}/mapsets/{mapset_name}/processing_async

        raster_layers : bool
        Returns
        -------
        base_url : str
            Return the url scheme for the mapset request
        """
        base_url = f"{actinia_url}/locations/{location_name}/mapsets"
        if mapset_name is not None:
            base_url = f"{base_url}/{mapset_name}"
            if isinstance(task, MAPSET_TASK):
                base_url = f"{base_url}/{task.value}"

        return base_url

    def info(self):
        """Get mapset info"""
        if self.projection is None or self.region is None:
            proc_res = self.request_info(
                self.name,
                self.__location_name,
                self.__actinia,
                self.__auth
            )
            self.projection = proc_res["projection"]
            self.region = Region(**proc_res["region"])
        return {"projection": self.projection, "region": self.region}

    def delete(self):
        """Deletes the mapset"""
        self.delete_mapset_request(
            self.name,
            self.__location_name,
            self.__actinia,
            self.__auth
        )
        del self.__actinia.locations[self.__location_name].mapsets[self.name]

    @classmethod
    def list_mapsets_request(cls, location_name, actinia, auth):
        """
        Lists mapsets within a location.

        Parameters
        ----------
        location_name : str
            The name of the location where the mapsets are located.
        actinia : Actinia
            An Actinia instance containing the url
        auth :
            Actinia authentication
        Returns
        -------
        mapsets : dict[mapset_name, Mapset]
            A dict of with keys equal to the mapset name and
            values set to the Mapset class instance.
        """
        url = cls.__request_url(actinia.url, location_name)
        resp = requests.get(url, auth=auth)
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")

        mapset_names = json.loads(resp.text)["process_results"]
        mapsets = {
            mname: Mapset(mname, location_name, actinia, auth)
            for mname in mapset_names
        }
        return mapsets

    @classmethod
    def create_mapset_request(cls, mapset_name, location_name, actinia, auth):
        """
        Creates a mapset within a location.

        Parameters
        ----------
        mapset_name : str
            The name of the created mapset.
        location_name : str
            The name of the location where the mapset is created
        actinia : Actinia
            An Actinia instance containing the url
        auth :
            Actinia authentication
        Returns
        -------
        Mapset
            A new mapset instance for the created mapset
        """
        url = cls.__request_url(actinia.url, location_name, mapset_name)
        resp = requests.post(url, auth=(auth))
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        return Mapset(mapset_name, location_name, actinia, auth)

    @classmethod
    def delete_mapset_request(cls, mapset_name, location_name, actinia, auth):
        """
        Delete a mapset within a location.

        Parameters
        ----------
        mapset_name : str
            The name of the mapset to delete
        location_name : str
            The name of the mapset's location
        actinia : Actinia
            An Actinia instance containing the url
        auth :
            Actinia authentication
        """
        url = cls.__request_url(actinia.url, location_name, mapset_name)
        resp = requests.delete(url, auth=(auth))
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        return None

    @classmethod
    def request_info(cls, mapset_name, location_name, actinia, auth):
        """
        Delete a mapset within a location.

        Parameters
        ----------
        mapset_name : str
            The name of mapset.
        location_name : str
            The name of the location
        actinia : Actinia
            An Actinia instance containing the url
        auth :
            Actinia authentication
        """
        url = cls.__request_url(
            actinia.url,
            location_name,
            mapset_name,
            MAPSET_TASK.INFO
        )
        resp = requests.get(url, auth=(auth))
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        proc_res = json.loads(resp.text)["process_results"]
        return proc_res

# TODO:
# * (/locations/{location_name}/mapsets/{mapset_name}/lock - GET, DELETE, POST)

# * /locations/{location_name}/mapsets/{mapset_name}/raster_layers
#      - DELETE, GET, PUT
# * /locations/{location_name}/mapsets/{mapset_name}/strds - GET
# * "/locations/{location_name}/mapsets/{mapset_name}/vector_layers"

# * (/locations/{location_name}/mapsets/{mapset_name}/processing
#          - POST (persistent, asyncron))
# * /locations/{location_name}/mapsets/{mapset_name}/processing_async
#          - POST (persistent, asyncron)
