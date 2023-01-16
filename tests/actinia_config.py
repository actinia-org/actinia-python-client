#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# Copyright (c) 2023 mundialis GmbH & Co. KG
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
__copyright__ = "Copyright 2023, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"


import os


localhost = True
if localhost:
    # localhost
    ACTINIA_BASEURL = "http://localhost:8088/"
    ACTINIA_VERSION = "v3"
    ACTINIA_AUTH = ("actinia-gdi", "actinia-gdi")
else:
    # actinia.mundialis.de
    ACTINIA_BASEURL = "https://actinia.mundialis.de/"
    ACTINIA_VERSION = "v3"
    ACTINIA_AUTH = (
        os.getenv("ACTINIA_USER", "demouser"),
        os.getenv("ACTINIA_PW", "gu3st!pa55w0rd")
    )

LOCATION_NAME = "nc_spm_08"
MAPSET_NAME = "PERMANENT"
RASTER_NAME = "zipcodes"
VECTOR_NAME = "boundary_county"
