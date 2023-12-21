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
__author__ = "Anika Weinmann and Corey White"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import json
import os
import requests
from enum import Enum, unique

from actinia.region import Region
from actinia.resources.logger import log
from actinia.raster import Raster
from actinia.vector import Vector
from actinia.utils import request_and_check
from actinia.job import Job
from actinia.utils import set_job_names


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

    def __request_url(actinia_url, location_name, mapset_name=None, task=None):
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
                self.name, self.__location_name, self.__actinia, self.__auth
            )
            self.projection = proc_res["projection"]
            self.region = Region(**proc_res["region"])
        return {"projection": self.projection, "region": self.region}

    def delete(self):
        """Deletes the mapset"""
        self.delete_mapset_request(
            self.name, self.__location_name, self.__actinia, self.__auth
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

        Raises
        ------
        Exception
            Error string with response status code
            and text if request fails.
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

        Raises
        ------
        Exception
            Error string with response status code
            and text if request fails.
        """
        # check if mapset exists
        existing_mapsets = cls.list_mapsets_request(
            location_name, actinia, auth
        )
        if mapset_name in existing_mapsets:
            log.warning(f"Mapset <{mapset_name}> already exists.")
            return existing_mapsets[mapset_name]

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

        Returns
        -------
        None

        Raises
        ------
        Exception
            Error string with response status code
            and text if request fails.
        """
        # check if mapset exists
        existing_mapsets = cls.list_mapsets_request(
            location_name, actinia, auth
        )
        if mapset_name not in existing_mapsets:
            log.warning(
                f"Mapset <{mapset_name}> does not exist and cannot be deleted."
            )
            return None

        url = cls.__request_url(actinia.url, location_name, mapset_name)
        resp = requests.delete(url, auth=(auth))
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        return None

    @classmethod
    def request_info(cls, mapset_name, location_name, actinia, auth):
        """
        Gets detailed info about a mapset.

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

        Returns
        -------
        dict
        Returns JSON process results if successful.

        Raises
        ------
        Exception
            Error string with response status code
            and text if request fails.
        """
        url = cls.__request_url(
            actinia.url, location_name, mapset_name, MAPSET_TASK.INFO
        )
        resp = requests.get(url, auth=(auth))
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        proc_res = json.loads(resp.text)["process_results"]
        return proc_res

    def __request_raster_layers(self):
        """
        Requests the raster layers in the mapset.

        :return: A list of the raster maps
        """
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/raster_layers"
        )
        resp = request_and_check(url, auth=self.__auth)
        raster_names = resp["process_results"]
        rasters = {
            mname: Raster(
                mname,
                self.__location_name,
                self.name,
                self.__actinia,
                self.__auth,
            )
            for mname in raster_names
        }
        self.raster_layers = rasters

    def get_raster_layers(self, force=False):
        """
        Return raster layers of the mapset
        """
        if self.raster_layers is None or force is True:
            self.__request_raster_layers()
        return self.raster_layers

    def __request_vector_layers(self):
        """
        Requests the vector layers in the mapset.

        :return: A list of the vector maps
        """
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/vector_layers"
        )
        resp = request_and_check(url, auth=self.__auth)
        vector_names = resp["process_results"]
        vectors = {
            mname: Vector(
                mname,
                self.__location_name,
                self.name,
                self.__actinia,
                self.__auth,
            )
            for mname in vector_names
        }
        self.vector_layers = vectors

    def get_vector_layers(self, force=False):
        """
        Return vector layers of the mapset
        """
        if self.vector_layers is None or force is True:
            self.__request_vector_layers()
        return self.vector_layers

    def upload_raster(self, layer_name, tif_file):
        """Upload GTiff as a raster layer
        Parameters:
            layer_name (string): Name for the raster layer to create
            tif_file (string): Path of the GTiff file to upload
        """
        files = {"file": (tif_file, open(tif_file, "rb"))}
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/raster_layers/{layer_name}"
        )
        resp = requests.post(
            url=url,
            files=files,
            auth=self.__auth,
        )
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        resp_dict = json.loads(resp.text)
        job = Job(
            f"raster_upload_{self.__location_name}_{self.name}_{layer_name}",
            self.__actinia,
            self.__auth,
            resp_dict,
        )
        job.poll_until_finished()
        if job.status != "finished":
            raise Exception(f"{job.status}: {job.message}")
        if self.raster_layers is None:
            self.get_raster_layers()
        self.raster_layers[layer_name] = Raster(
            layer_name,
            self.__location_name,
            self.name,
            self.__actinia,
            self.__auth,
        )

    def delete_raster(self, layer_name):
        """Delete a raster layer"""
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/raster_layers/{layer_name}"
        )
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
        log.info(f"Raster <{layer_name}> successfully deleted")

    def upload_vector(self, layer_name, vector_file):
        """Upload vector file (GPKG, zipped Shapefile or GeoJSON) as a vector
        layer.
        Parameters:
            layer_name (string): Name for the vector layer to create
            vector_file (string): Path of the GPKG/zipped Shapefile or GeoJSON
                                  to upload
        """
        files = {"file": (vector_file, open(vector_file, "rb"))}
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/vector_layers/{layer_name}"
        )
        resp = requests.post(
            url=url,
            files=files,
            auth=self.__auth,
        )
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        resp_dict = json.loads(resp.text)
        job = Job(
            f"vector_upload_{self.__location_name}_{self.name}_{layer_name}",
            self.__actinia,
            self.__auth,
            resp_dict,
        )
        job.poll_until_finished()
        if job.status != "finished":
            raise Exception(f"{job.status}: {job.message}")
        if self.vector_layers is None:
            self.get_vector_layers()
        self.vector_layers[layer_name] = Vector(
            layer_name,
            self.__location_name,
            self.name,
            self.__actinia,
            self.__auth,
        )

    def delete_vector(self, layer_name):
        """Delete a vector layer"""
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/vector_layers/{layer_name}"
        )
        resp = requests.delete(
            url=url,
            auth=self.__auth,
        )
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        if self.vector_layers is None:
            self.get_vector_layers()
        else:
            del self.vector_layers[layer_name]
        log.info(f"Vector <{layer_name}> successfully deleted")

    # TODO: * (/locations/{location_name}/mapsets/{mapset_name}/processing
    #          - POST (persistent, asyncron))
    # * /locations/{location_name}/mapsets/{mapset_name}/processing_async
    #          - POST (persistent, asyncron)
    def create_processing_job(self, pc, name=None):
        """
        Creates a processing job with a given PC.
        """
        # set name
        orig_name, name = set_job_names(name)
        # set endpoint in url
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/processing_async"
        )
        # make POST request
        postkwargs = dict()
        postkwargs["headers"] = self.__actinia.headers
        postkwargs["auth"] = self.__auth
        if isinstance(pc, str):
            if os.path.isfile(pc):
                with open(pc, "r") as pc_file:
                    postkwargs["data"] = pc_file.read()
            else:
                postkwargs["data"] = pc
        elif isinstance(pc, dict):
            postkwargs["data"] = json.dumps(pc)
        else:
            raise Exception("Given process chain has no valid type.")

        try:
            actiniaResp = requests.post(url, **postkwargs)
        except requests.exceptions.ConnectionError as e:
            raise e
        # create a job
        resp = json.loads(actiniaResp.text)
        job = Job(orig_name, self.__actinia, self.__auth, resp)
        self.__actinia.jobs[name] = job
        return job


# TODO:
# * (/locations/{location_name}/mapsets/{mapset_name}/lock - GET, DELETE, POST)

# * /locations/{location_name}/mapsets/{mapset_name}/raster_layers
#      - DELETE, PUT
# * /locations/{location_name}/mapsets/{mapset_name}/strds - GET
# * "/locations/{location_name}/mapsets/{mapset_name}/vector_layers"
