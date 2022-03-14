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

# import json
# import requests
#
# from actinia.region import Region


class Mapset:
    def __init__(self, name, actinia, auth):
        self.name = name
        self.projection = None
        self.region = None
        self.__actinia = actinia
        self.__auth = auth
        self.raster_layers = None
        self.vector_layers = None
        self.strds = None


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
