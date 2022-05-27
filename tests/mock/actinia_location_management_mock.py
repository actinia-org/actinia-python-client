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
__maintainer__ = "testuser Weinmann"

from copy import deepcopy

from .actinia_mock import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    fill_basic_frame,
)


location_creation_resp = {
    "accept_datetime": "2022-05-27 07:44:19.428476",
    "accept_timestamp": 1653637459.4284744,
    "api_info": {
        "endpoint": "locationmanagementresourceadmin",
        "method": "POST",
        "path": f"/api/{ACTINIA_VERSION}/locations/test_location",
        "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/"
                       "test_location"
    },
    "datetime": "2022-05-27 07:44:20.738901",
    "http_code": 200,
    "message": "Location <test_location> successfully created",
    "process_chain_list": [{
        "1": {
            "flags": "t",
            "inputs": {
                "epsg": "25832",
                "location": "test_location"
            },
            "module": "g.proj"
        }
    }],
    "process_log": [{
        "executable": "g.proj",
        "id": "1",
        "parameter": ["epsg=25832", "location=test_location", "-t"],
        "return_code": 0,
        "run_time": 0.30111145973205566,
        "stderr": ["Location <test_location> created", "You can switch to the "
                   "new location by", "`g.mapset mapset=PERMANENT "
                   "location=test_location`", ""],
        "stdout": ""
    }],
    "process_results": {},
    "progress": {
        "num_of_steps": 1,
        "step": 1
    },
    "resource_id": "resource_id-21852f11-8f39-4af1-91c2-93c83185ba61",
    "status": "finished",
    "time_delta": 1.310459852218628,
    "timestamp": 1653637460.738866,
    "urls": {
        "resources": [],
        "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser"
                  "/resource_id-21852f11-8f39-4af1-91c2-93c83185ba61"
    },
    "user_id": "testuser"
}

delete_location_resp = {
    "message": "location test_location deleted",
    "status": "success"
}

get_locations_resp = {
    "locations": ["latlong_wgs84", "ECAD", "nc_spm_08"],
    "status": "success",
}

p_result_location_info = {
    "projection": '"PROJCRS["NAD83(HARN) / North Carolina",BASEGEOGCRS'
    '["NAD83(HARN)",DATUM["NAD83 (High Accuracy Reference Network)",'
    'ELLIPSOID["GRS 1980",6378137,298.257222101,LENGTHUNIT'
    '["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",'
    '0.0174532925199433]],ID["EPSG",4152]],CONVERSION["SPCS83 North '
    'Carolina zone (meters)",METHOD["Lambert Conic Conformal (2SP)",'
    'ID["EPSG",9802]],PARAMETER["Latitude of false origin",33.75,'
    'ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8821]],'
    'PARAMETER["Longitude of false origin",-79,ANGLEUNIT["degree",'
    '0.0174532925199433],ID["EPSG",8822]],PARAMETER["Latitude of 1st '
    'standard parallel",36.1666666666667,ANGLEUNIT["degree",'
    '0.0174532925199433],ID["EPSG",8823]],PARAMETER["Latitude of 2nd '
    'standard parallel",34.3333333333333,ANGLEUNIT["degree",'
    '0.0174532925199433],ID["EPSG",8824]],PARAMETER["Easting at false '
    'origin",609601.22,LENGTHUNIT["metre",1],ID["EPSG",8826]],'
    'PARAMETER["Northing at false origin",0,LENGTHUNIT["metre",1],'
    'ID["EPSG",8827]]],CS[Cartesian,2],AXIS["easting (X)",east,'
    'ORDER[1],LENGTHUNIT["metre",1]],AXIS["northing (Y)",north,'
    'ORDER[2],LENGTHUNIT["metre",1]],USAGE[SCOPE["unknown"],'
    'AREA["USA - North Carolina"],BBOX[33.83,-84.33,36.59,-75.38]],'
    'ID["EPSG",3358]]',
    "region": {
        "b": 0,
        "cells": 29535,
        "cells3": 29535,
        "cols": 179,
        "cols3": 179,
        "depths": 1,
        "e": 639530,
        "ewres": 10,
        "ewres3": 10,
        "n": 221230,
        "nsres": 10,
        "nsres3": 10,
        "projection": 99,
        "rows": 165,
        "rows3": 165,
        "s": 219580,
        "t": 1,
        "tbres": 1,
        "w": 637740,
        "zone": 0,
    },
}
location_get_info_resp = fill_basic_frame(p_result_location_info)
