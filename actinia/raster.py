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

from actinia.region import Region
from actinia.utils import request_and_check


class Raster:
    def __init__(self, name, location_name, mapset_name, actinia, auth):
        self.name = name
        self.__location_name = location_name
        self.__mapset_name = mapset_name
        self.__actinia = actinia
        self.__auth = auth
        self.region = None
        self.info = None

    def get_info(self):
        """Return the information of the raster map"""
        if self.info is None:
            url = (
                f"{self.__actinia.url}/locations/{self.__location_name}/"
                f"mapsets/{self.__mapset_name}/raster_layers/{self.name}"
            )
            resp = request_and_check(url, self.__auth)
            r_info = resp["process_results"]
            self.info = r_info

            self.region = Region(
                zone=None,
                projection=None,
                n=r_info["north"],
                s=r_info["south"],
                e=r_info["east"],
                w=r_info["west"],
                t=None,
                b=None,
                nsres=r_info["nsres"],
                ewres=r_info["ewres"],
                nsres3=None,
                ewres3=None,
                tbres=None,
                rows=r_info["rows"],
                cols=r_info["cols"],
                rows3=None,
                cols3=None,
                depths=None,
                cells=r_info["cells"],
                cells3=None,
            )
        return self.info
