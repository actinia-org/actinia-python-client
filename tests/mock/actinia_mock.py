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

ACTINIA_BASEURL = "http://localhost:8088"
ACTINIA_VERSION = "v3"
ACTINIA_TEST_AUTH = ("user", "pw")
ACTINIA_API_PREFIX = "latest"

version_resp_text = {
    "grass_version": {
        "build_date": "2021-09-21",
        "build_off_t_size": "8",
        "build_platform": "x86_64-pc-linux-musl",
        "date": "2021",
        "gdal": "3.1.4",
        "geos": "3.8.1",
        "libgis_date": "2021-09-21T10:04:04+00:00",
        "libgis_revision": "2021-09-21T10:04:04+00:00",
        "proj": "7.0.1",
        "revision": "7388b3f",
        "sqlite": "3.32.1",
        "version": "7.8.6dev",
    },
    "plugin_versions": {
        "actinia_metadata_plugin": "1.0.0",
        "actinia_module_plugin": "2.2.0",
        "actinia_satellite_plugin": "0.0.3",
        "actinia_statistic_plugin": "0.0.3",
    },
    "plugins": "actinia_statistic_plugin,actinia_satellite_plugin,"
               "actinia_metadata_plugin,actinia_module_plugin",
    "python_version": "3.8.5 (default, Jul 20 2020, 23:11:29) - [GCC 9.3.0]",
    "version": "1.2.1",
}


def fill_basic_frame(
    process_results={},
    process_chain=None,
    process_log=None,
    progress=False,
    status="finished",
):
    basic_frame = {
        "accept_datetime": "2022-03-07 13:46:52.249333",
        "accept_timestamp": 1646660812.2493308,
        "api_info": {
            "endpoint": "locationmanagementresourceuser",
            "method": "GET",
            "path": f"/api/{ACTINIA_VERSION}/locations/nc_spm_08/info",
            "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations"
                           "/nc_spm_08/info",
        },
        "datetime": "2022-03-07 13:46:54.791928",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_chain_list": process_chain,
        "process_results": process_results,
        "resource_id": "resource_id-573cdb12-2d35-4bf1-8f0b-61443ea07d25",
        "status": status,
        "time_delta": 2.542658805847168,
        "timestamp": 1646660814.7918556,
        "urls": {
            "resources": [],
            "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/"
                      "demouser/resource_id-573cdb12-2d35-4bf1-8f0b-"
                      "61443ea07d25",
        },
        "user_id": "demouser",
    }
    if process_log is not None:
        basic_frame["process_log"] = process_log
    if progress is True:
        basic_frame["progress"] = {"num_of_steps": 2, "step": 2}
    return basic_frame


# p_result_location_info = {
#     "projection": '"PROJCRS["NAD83(HARN) / North Carolina",BASEGEOGCRS'
#     '["NAD83(HARN)",DATUM["NAD83 (High Accuracy Reference Network)",'
#     'ELLIPSOID["GRS 1980",6378137,298.257222101,LENGTHUNIT'
#     '["metre",1]]],PRIMEM["Greenwich",0,ANGLEUNIT["degree",'
#     '0.0174532925199433]],ID["EPSG",4152]],CONVERSION["SPCS83 North '
#     'Carolina zone (meters)",METHOD["Lambert Conic Conformal (2SP)",'
#     'ID["EPSG",9802]],PARAMETER["Latitude of false origin",33.75,'
#     'ANGLEUNIT["degree",0.0174532925199433],ID["EPSG",8821]],'
#     'PARAMETER["Longitude of false origin",-79,ANGLEUNIT["degree",'
#     '0.0174532925199433],ID["EPSG",8822]],PARAMETER["Latitude of 1st '
#     'standard parallel",36.1666666666667,ANGLEUNIT["degree",'
#     '0.0174532925199433],ID["EPSG",8823]],PARAMETER["Latitude of 2nd '
#     'standard parallel",34.3333333333333,ANGLEUNIT["degree",'
#     '0.0174532925199433],ID["EPSG",8824]],PARAMETER["Easting at false '
#     'origin",609601.22,LENGTHUNIT["metre",1],ID["EPSG",8826]],'
#     'PARAMETER["Northing at false origin",0,LENGTHUNIT["metre",1],'
#     'ID["EPSG",8827]]],CS[Cartesian,2],AXIS["easting (X)",east,'
#     'ORDER[1],LENGTHUNIT["metre",1]],AXIS["northing (Y)",north,'
#     'ORDER[2],LENGTHUNIT["metre",1]],USAGE[SCOPE["unknown"],'
#     'AREA["USA - North Carolina"],BBOX[33.83,-84.33,36.59,-75.38]],'
#     'ID["EPSG",3358]]',
#     "region": {
#         "b": 0,
#         "cells": 29535,
#         "cells3": 29535,
#         "cols": 179,
#         "cols3": 179,
#         "depths": 1,
#         "e": 639530,
#         "ewres": 10,
#         "ewres3": 10,
#         "n": 221230,
#         "nsres": 10,
#         "nsres3": 10,
#         "projection": 99,
#         "rows": 165,
#         "rows3": 165,
#         "s": 219580,
#         "t": 1,
#         "tbres": 1,
#         "w": 637740,
#         "zone": 0,
#     },
# }
# location_get_info_resp = fill_basic_frame(p_result_location_info)


p_result_get_mapsets = [
    "PERMANENT",
    "True",
    "landsat",
    "modis_lst",
    "test_mapset"
]
location_get_mapset_resp = fill_basic_frame(p_result_get_mapsets)

start_job_resp = fill_basic_frame(process_results={}, status="accepted")
job_poll_resp = fill_basic_frame(process_results={}, progress=True)
