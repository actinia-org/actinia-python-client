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
import os
import sys

from actinia.resources.logger import log
from actinia.region import Region
from actinia.mapset import Mapset
from actinia.job import Job
from actinia.utils import set_job_names


class Location:
    def __init__(self, name, actinia, auth):
        self.name = name
        self.projection = None
        self.region = None
        self.__actinia = actinia
        self.__auth = auth
        self.mapsets = dict()

    def __request_info(self):
        """
        Requests location information
        """
        if self.__actinia.user is None:
            raise Exception("Authentication is not set.")

        url = f"{self.__actinia.url}/locations/{self.name}/info"
        resp = requests.get(url, auth=(self.__auth))
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")

        proc_res = json.loads(resp.text)["process_results"]
        self.projection = proc_res["projection"]
        self.region = Region(**proc_res["region"])

    def get_info(self):
        """
        Return location information
        """
        if self.projection is None or self.region is None:
            self.__request_info()
        return {"projection": self.projection, "region": self.region}

    def __request_mapsets(self):
        """
        Requests the mapsets in the given location.

        :return: A list of the mapset names
        """
        self.mapsets = Mapset.list_mapsets_request(
            self.name, self.__actinia, self.__auth
        )
        return self.mapsets

    def delete(self):
        """Delete a location via delete request."""
        url = f"{self.__actinia.url}/locations/{self.name}"
        resp = requests.delete(url, auth=self.__auth)
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        del self.__actinia.locations[self.name]

    def get_mapsets(self):
        """
        Return mapsets
        """
        if self.mapsets is None or len(self.mapsets) == 0:
            self.__request_mapsets()
        return self.mapsets

    def create_mapset(self, name):
        """
        Creates a mapset within the location.
        """
        if self.mapsets is None or len(self.mapsets) == 0:
            self.__request_mapsets()
        mapset = Mapset.create_mapset_request(
            name, self.name, self.__actinia, self.__auth
        )
        # We could also fetch data from the server again
        # with self.__request_mapsets() to ensure data is stale
        if name not in self.mapsets:
            self.mapsets[name] = mapset
        return mapset

    def delete_mapset(self, name):
        """
        Deletes a mapset and returns an updated mapset list for the location.
        """
        if self.mapsets is None or len(self.mapsets) == 0:
            self.__request_mapsets()
        Mapset.delete_mapset_request(
            name, self.name, self.__actinia, self.__auth
        )
        if name is name in self.mapsets:
            del self.mapsets[name]
        return self.mapsets

    def __validate_process_chain(self, pc, type):
        url = f"{self.__actinia.url}/locations/{self.name}/"
        if type == "async":
            url += "process_chain_validation_async"
        elif type == "sync":
            url += "process_chain_validation_sync"
        else:
            raise Exception("Type is not async or sync")
        resp = requests.post(
            url,
            auth=self.__auth,
            headers=self.__actinia.headers,
            data=json.dumps(pc),
        )
        return resp

    def validate_process_chain_sync(self, pc):
        """Validate a process chain (sync)."""
        resp = self.__validate_process_chain(pc, "sync")
        if resp.status_code == 200:
            log.info(json.loads(resp.text)["message"])
        elif resp.status_code == 400:
            msg = f"Validation error: {json.loads(resp.text)['message']}"
            log.error(msg, file=sys.stderr)
        else:
            raise Exception(f"Error {resp.status_code}: {resp.text}")

    def validate_process_chain_async(self, pc, name=None):
        """Validate a process chain (async)."""
        actiniaResp = self.__validate_process_chain(pc, "async")
        orig_name, name = set_job_names(name, "unknown_validation_job")
        if actiniaResp.status_code != 200:
            raise Exception(
                f"Error {actiniaResp.status_code}: {actiniaResp.text}"
            )
        resp = json.loads(actiniaResp.text)
        job = Job(orig_name, self.__actinia, self.__auth, resp)
        self.__actinia.jobs[name] = job
        return job

    # TODO: * /locations/{location_name}/processing_async_export
    #            - POST (ephemeral database)
    # * (/locations/{location_name}/processing_export
    #            - POST (ephemeral database))
    def create_processing_export_job(self, pc, name=None):
        """
        Creates a processing_export job with a given PC.
        """
        # set name
        orig_name, name = set_job_names(name)
        # set endpoint in url
        url = (
            f"{self.__actinia.url}/locations/{self.name}/"
            "processing_async_export"
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
# * /locations/{location_name}/process_chain_validation_async - POST
# * /locations/{location_name}/process_chain_validation_sync - POST
# * /locations/{location_name}/processing_async_export
#               - POST (ephemeral database)
# * (/locations/{location_name}/processing_export - POST (ephemeral database))
# * (/locations/{location_name}/processing_async_export_gcs - POST)
# * (/locations/{location_name}/processing_async_export_s3 - POST)
