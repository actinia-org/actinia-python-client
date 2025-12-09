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

import json

from actinia.resources.logger import log
from actinia.region import Region
from actinia.utils import request_and_check


class Vector:
    def __init__(self, name, location_name, mapset_name, actinia, auth):
        self.name = name
        self.__location_name = location_name
        self.__mapset_name = mapset_name
        self.__actinia = actinia
        self.__auth = auth
        self.region = None
        self.info = None

    def get_info(self):
        """Return the information of the vector map"""
        if self.info is None:
            url = (
                f"{self.__actinia.url}/locations/{self.__location_name}/"
                f"mapsets/{self.__mapset_name}/vector_layers/{self.name}"
            )
            v_info = request_and_check(
                "GET",
                url,
                **{"auth": self.__auth, "timeout": self.__actinia.timeout},
            )["process_results"]
            self.info = v_info

            self.region = Region(
                zone=None,
                projection=None,
                n=v_info["north"],
                s=v_info["south"],
                e=v_info["east"],
                w=v_info["west"],
                t=v_info["top"],
                b=v_info["bottom"],
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
                cells3=None,
            )
        log.info(json.dumps(self.info, indent=4))
        return self.info


# TODO:
# * /locations/{location_name}/mapsets/{mapset_name}/vector_layers
#          - DELETE, GET, PUT
# * /locations/{location_name}/mapsets/{mapset_name}/vector_layers/
#          {vector_name} - GET, DELETE, POST
# * /locations/{location_name}/mapsets/{mapset_name}/vector_layers/
#          {vector_name}/render - GET
