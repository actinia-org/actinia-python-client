#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# SPDX-FileCopyrightText: (c) 2022 mundialis GmbH & Co. KG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#######

__license__ = "GPL-3.0-or-later"
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
            r_info = request_and_check(
                "GET",
                url,
                **{"auth": self.__auth, "timeout": self.__actinia.timeout},
            )["process_results"]
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
