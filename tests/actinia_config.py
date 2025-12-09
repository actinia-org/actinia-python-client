#!/usr/bin/env python
"""Configuration for actinia-python-client tests.

actinia-python-client is a python client for actinia - an open source REST
API for scalable, distributed, high performance processing of geographical
data that uses GRASS GIS for computational tasks.

Copyright (c) 2023-2025 mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2023-2025, mundialis GmbH & Co. KG"
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
        os.getenv("ACTINIA_PW", "gu3st!pa55w0rd"),
    )

LOCATION_NAME = "nc_spm_08"
MAPSET_NAME = "PERMANENT"
RASTER_NAME = "elevation"
VECTOR_NAME = "boundary_county"
STRDS_NAME = "sample_strds"
