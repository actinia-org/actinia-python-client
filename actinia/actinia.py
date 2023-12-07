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
import re
import requests

from actinia.location import Location
from actinia.resources.templating import tplEnv
from actinia.resources.logger import log


class Actinia:
    def __init__(
        self,
        url="https://actinia.mundialis.de/",
        api_version="latest",
        user=None,
        pw=None,
    ):
        self.api_prefix = api_version
        self.base_url = url
        self.headers = {"content-type": "application/json; charset=utf-8"}
        self.user = None
        self.__password = None
        self.__auth = None
        if user and pw:
            self.set_authentication(user, pw)
        self.locations = dict()
        self.__set_url()
        self.__check_version()
        self.jobs = dict()

    def __set_url(self):
        if self.api_prefix == "latest":
            self.url = f"{self.base_url}/{self.api_prefix}"
        elif self.api_prefix.startswith("api/"):
            self.url = f"{self.base_url}/{self.api_prefix}"
        else:
            self.url = f"{self.base_url}/api/{self.api_prefix}"

    def __check_version(self):
        version_url = f"{self.url}/version"
        resp = requests.get(version_url)
        if resp.status_code != 200:
            raise Exception("Connection to actinia server failed!")

        data = json.loads(resp.text)

        if len(data) > 2:
            log.debug(f"{self.url} is working and will be used.")
            # TODO schöneres format: return version
            return data

        if data[1] != 200:
            if "links" in data[0]:
                if "links" in data[0]:
                    base = self.base_url.split("://")[1]
                    self.api_prefix = re.findall(
                        rf"{base}/(.*?)/version", data[0]["links"][0]
                    )[0]
                    self.__set_url()
                    log.warning(f"Using actinia <{self.url}>")
                else:
                    self.api_version = "v1"
                    self.__check_version()
            else:
                raise Exception(
                    f"Connection to actinia server <{self.url}> failed!"
                )

    def get_version(self):
        """
        Requests versions of GRASS GIS, actinia-core and installed plugins
        :return: dict with version information
        """

        version_url = f"{self.url}/version"
        resp = requests.get(version_url)
        if resp.status_code != 200:
            raise Exception("Connection to actinia server failed!")
        data = json.loads(resp.text)
        return data

    def __check_auth(self):
        url = f"{self.url}/locations"
        resp = requests.get(url, auth=(self.__auth))
        if resp.status_code == 401:
            raise Exception(
                "Wrong user or password. Please check your inputs."
            )
        elif resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")
        else:
            log.debug(f"{self.user} is logged in.")

    def set_authentication(self, user, pw):
        """
        Set the user and password for the actinia instance and checks if the
        logging is working via the locations endpoint.

        :param user: String with username
        :param pw: String with user password
        :raises: exception if the user cannot log in
        """
        self.user = user
        self.__password = pw
        self.__auth = (user, pw)
        try:
            self.__check_auth()
        except Exception as e:
            self.user = None
            self.__password = None
            self.__auth = None
            raise e

    def get_locations(self):
        if len(self.locations) == 0:
            self.__request_locations()
        return self.locations

    def __request_locations(self):
        """
        Requests the locations in the actinia instance.

        :return: A dict of the locations with the location names as key
        """
        if self.user is None:
            raise Exception("Authentication is not set.")

        url = f"{self.url}/locations"
        resp = requests.get(url, auth=(self.__auth))
        if resp.status_code != 200:
            raise Exception(f"Error {resp.status_code}: {resp.text}")

        loc_names = json.loads(resp.text)["locations"]
        loc = {
            lname: Location(lname, self, self.__auth) for lname in loc_names
        }
        self.locations = loc

    def create_location(self, name, epsgcode):
        """
        Creates a new location with given name and EPSG code via post request.

        :return: The created location
        """
        if name in self.locations:
            log.warning(f"Location <{name}> already exists.")
            return self.locations[name]
        tpl = tplEnv.get_template("create_location.json")
        postbody = tpl.render(epsgcode=epsgcode)

        url = f"{self.url}/locations/{name}"
        resp = requests.post(
            url,
            auth=(self.__auth),
            headers=self.headers,
            data=postbody,
        )
        if resp.status_code != 200:
            try:
                msg = json.loads(resp.text)["message"]
            except Exception:
                msg = resp.text
            raise Exception(f"Error {resp.status_code}: {msg}")

        location = Location(name, self, self.__auth)
        if len(self.locations) == 0:
            self.__request_locations()
        self.locations[name] = location

        return location


# TODO:
# * /resource_storage - GET, DELETE
# * /resources/{user_id} - GET, DELETE
# * /resources/{user_id}/{resource_id} - DELETE, GET, PUT
