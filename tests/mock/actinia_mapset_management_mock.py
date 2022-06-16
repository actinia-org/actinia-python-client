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
__author__ = "Corey White"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

from .actinia_mock import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION
)

mapset_creation_resp = {
    "accept_datetime": "2022-05-27 07:44:19.428476",
    "accept_timestamp": 1653637459.4284744,
    "api_info": {
        "endpoint": "mapsetmanagementresourceadmin",
        "method": "POST",
        "path": f"/api/{ACTINIA_VERSION}/locations/test_location/" +
                "mapsets/test_mapset",
        "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/"
                       "test_location/mapsets/test_mapset"
    },
    "datetime": "2022-05-27 07:44:20.738901",
    "http_code": 200,
    "message": "Mapset <test_mapset> successfully created.",
    "process_chain_list": [{
        "1": {
            "flags": "l",
            "module": "g.mapsets"
        }
    }],
    "process_log": [{
        "executable": "g.mapsets",
        "id": "1",
        "parameter": ["-l"],
        "return_code": 0,
        "run_time": 0.05029106140136719,
        "stderr": ["Available mapsets:", ""],
        "stdout": "PERMANENT test_mapset\n"
    }],
    "process_results": {},
    "progress": {
        "num_of_steps": 1,
        "step": 1
    },
    "resource_id": "resource_id-b4a57ebe-b3e9-4e6a-bab6-c01e7b97f670",
    "status": "finished",
    "time_delta": 1.310459852218628,
    "timestamp": 1653637460.738866,
    "urls": {
        "resources": [],
        "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser"
                  "/resource_id-b4a57ebe-b3e9-4e6a-bab6-c01e7b97f670"
    },
    "user_id": "testuser"
}

delete_mapset_resp = {
    "response": {
        "accept_datetime": "2022-06-09 00:04:15.807052",
        "accept_timestamp": 1654733055.807051,
        "api_info": {
            "endpoint": "mapsetmanagementresourceadmin",
            "method": "DELETE",
            "path": f"/api/{ACTINIA_VERSION}/locations/test_location/" +
                    "mapsets/test_mapset",
            "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/" +
                    "locations/test_location/mapsets/test_mapset"
        },
        "datetime": "2022-06-09 00:04:15.866212",
        "http_code": 200,
        "message": "Mapset <test_mapset> successfully removed.",
        "process_chain_list": [],
        "process_log": [],
        "process_results": {},
        "progress": {
            "num_of_steps": 0,
            "step": 0
        },
        "resource_id": "resource_id-af7aa2aa-5db0-4e8b-b921-05a7b99ac0c5",
        "status": "finished",
        "time_delta": 0.059175729751586914,
        "timestamp": 1654733055.8661997,
        "urls": {
            "resources": [],
            "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/" +
                       "testuser" +
                       "/resource_id-af7aa2aa-5db0-4e8b-b921-05a7b99ac0c5"
        },
        "user_id": "testuser"
    }
}

get_mapsets_resp = {
    "response": {
        "accept_datetime": "2022-06-08 23:47:58.962452",
        "accept_timestamp": 1654732078.9624505,
        "api_info": {
            "endpoint": "listmapsetsresource",
            "method": "GET",
            "path": "/api/v3/locations/test_location/mapsets",
            "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/" +
            "locations/test_location/mapsets"
        },
        "datetime": "2022-06-08 23:47:59.118004",
        "http_code": 200,
        "message": "Processing successfully finished",
        "process_chain_list": [
            {
                "1": {
                    "flags": "l",
                    "inputs": {
                        "separator": "newline"
                    },
                    "module": "g.mapsets"
                    }
                }
            ],
        "process_log": [
                {
                    "executable": "g.mapsets",
                    "id": "1",
                    "parameter": [
                        "separator=newline",
                        "-l"
                    ],
                    "return_code": 0,
                    "run_time": 0.05015826225280762,
                    "stderr": ["Available mapsets:", ""],
                    "stdout": "test_mapset\n"
                }
            ],
        "process_results": ["PERMANENT", "test_mapset"],
        "progress": {
            "num_of_steps": 1, "step": 1
        },
        "resource_id": "resource_id-ba4de6ee-733c-4c29-887d-2d6c14dbd17c",
        "status": "finished",
        "time_delta": 0.15557193756103516,
        "timestamp": 1654732079.1179929,
        "urls": {
            "resources": [],
            "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/" +
                  "testuser/resource_id-ba4de6ee-733c-4c29-887d-2d6c14dbd17c"
        },
        "user_id": "testuser"
        }
    }


mapset_get_info_resp = {
    "accept_datetime": "2022-06-09 06:12:43.495084",
    "accept_timestamp": 1654755163.4950836,
    "api_info": {
        "endpoint": "mapsetmanagementresourceuser",
        "method": "GET",
        "path": f"/api/{ACTINIA_VERSION}/locations/test_location/mapsets/" +
                "test_mapset/info/",
        "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/" +
                "test_location/mapsets/test_mapset/info/"
    },
    "datetime": "2022-06-09 06:12:43.698443",
    "http_code": 200,
    "message": "Processing successfully finished",
    "process_chain_list": [
        {
            "1": {
                "flags": "ug3",
                "module": "g.region"
            },
            "2": {
                "flags": "fw",
                "module": "g.proj"
            }
        }
    ],
    "process_log": [
        {
            "executable": "g.region",
            "id": "1",
            "parameter": [
                "-ug3"
            ],
            "return_code": 0,
            "run_time": 0.05020761489868164,
            "stderr": [
                ""
            ],
            "stdout": "projection=99\nzone=0\nn=1\ns=0\nw=0\ne=1\nt=1\n" +
            "b=0\nnsres=1\nnsres3=1\newres=1\newres3=1\ntbres=1\nrows=1\n" +
            "rows3=1\ncols=1\ncols3=1\ndepths=1\ncells=1\ncells3=1\n"
        },
        {
            "executable": "g.proj",
            "id": "2",
            "parameter": [
                "-fw"
            ],
            "return_code": 0,
            "run_time": 0.10024547576904297,
            "stderr": [
                ""
            ],
            "stdout": "PROJCRS[\"NAD83(HARN) / North Carolina\",BASEGEOGCRS" +
            "[\"NAD83(HARN)\",DATUM[\"NAD83 (High Accuracy Reference" +
            "Network)\",ELLIPSOID[\"GRS 1980\",6378137,298.257222101," +
            "LENGTHUNIT[\"metre\",1]]],PRIMEM[\"Greenwich\",0,ANGLEUNIT" +
            "[\"degree\",0.0174532925199433]],ID[\"EPSG\",4152]],CONVERSION" +
            "[\"SPCS83 North Carolina zone (meters)\",METHOD[\"Lambert Conic" +
            "Conformal (2SP)\",ID[\"EPSG\",9802]],PARAMETER[\"Latitude of" +
            "false origin\",33.75,ANGLEUNIT[\"degree\",0.0174532925199433]" +
            ",ID[\"EPSG\",8821]],PARAMETER[\"Longitude of false origin\"," +
            "-79,ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8822" +
            "]],PARAMETER[\"Latitude of 1st standard parallel\"," +
            "36.1666666666667,ANGLEUNIT[\"degree\",0.0174532925199433]," +
            "ID[\"EPSG\",8823]],PARAMETER[\"Latitude of 2nd standard " +
            "parallel\",34.3333333333333,ANGLEUNIT[\"degree\"," +
            "0.0174532925199433],ID[\"EPSG\",8824]],PARAMETER[\"Easting " +
            "at false origin\",609601.22,LENGTHUNIT[\"metre\",1],ID[\"EP" +
            "SG\",8826]],PARAMETER[\"Northing at falseorigin\",0,LENGTH" +
            "UNIT[\"metre\",1],ID[\"EPSG\",8827]]],CS[Cartesian,2]," +
            "AXIS[\"easting (X)\",east,ORDER[1],LENGTHUNIT[\"metre\",1]]" +
            ",AXIS[\"northing (Y)\",north,ORDER[2],LENGTHUNIT" +
            "[\"metre\",1]],USAGE[SCOPE[\"Engineering survey, topographic" +
            "mapping.\"],AREA[\"United States (USA) - North Carolina -" +
            "counties of Alamance; Alexander; Alleghany; Anson; " +
            "Ashe; Avery; Beaufort; Bertie; Bladen; Brunswick; " +
            "Buncombe; Burke; Cabarrus; Caldwell; Camden; " +
            "Carteret; Caswell; Catawba; Chatham; Cherokee; Chowan; Clay; " +
            "Cleveland; Columbus; Craven; Cumberland; Currituck; Dare; " +
            "Davidson; Davie; Duplin; Durham; Edgecombe; Forsyth; Franklin; " +
            "Gaston; Gates; Graham; Granville; Greene; Guilford; Halifax; " +
            "Harnett; Haywood; Henderson; Hertford; Hoke; Hyde; Iredell; " +
            "Jackson; Johnston; Jones; Lee; Lenoir; Lincoln; Macon; " +
            "Madison; Martin; McDowell; Mecklenburg; Mitchell; Montgomery; " +
            "Moore; Nash; New Hanover; Northampton; Onslow; Orange; " +
            "Pamlico; Pasquotank; Pender; Perquimans; Person; Pitt; Polk; " +
            "Randolph; Richmond; Robeson; Rockingham; Rowan; Rutherford; " +
            "Sampson; Scotland; Stanly; Stokes; Surry; Swain; Transylvania; " +
            "Tyrrell; Union; Vance; Wake; Warren; Washington; Watauga; " +
            "Wayne; Wilkes; Wilson; Yadkin; Yancey.\"],BBOX[33.83,-84.33," +
            "36.59,-75.38]],ID[\"EPSG\",3358]]\n",
        }
    ],
    "process_results": {
        "projection":  "PROJCRS[\"NAD83(HARN) / North Carolina\",BASEGEOGCRS" +
        "[\"NAD83(HARN)\",DATUM[\"NAD83 (High Accuracy Reference" +
        "Network)\",ELLIPSOID[\"GRS 1980\",6378137,298.257222101," +
        "LENGTHUNIT[\"metre\",1]]],PRIMEM[\"Greenwich\",0,ANGLEUNIT" +
        "[\"degree\",0.0174532925199433]],ID[\"EPSG\",4152]],CONVERSION" +
        "[\"SPCS83 North Carolina zone (meters)\",METHOD[\"Lambert Conic" +
        "Conformal (2SP)\",ID[\"EPSG\",9802]],PARAMETER[\"Latitude of" +
        "false origin\",33.75,ANGLEUNIT[\"degree\",0.0174532925199433],ID" +
        "[\"EPSG\",8821]],PARAMETER[\"Longitude of false origin\",-79," +
        "ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8822]]," +
        "PARAMETER[\"Latitude of 1st standard parallel\",36.1666666666667," +
        "ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8823]]," +
        "PARAMETER[\"Latitude of 2nd standard parallel\",34.3333333333333" +
        ",ANGLEUNIT[\"degree\",0.0174532925199433],ID[\"EPSG\",8824]]," +
        "PARAMETER[\"Easting at false origin\",609601.22,LENGTHUNIT" +
        "[\"metre\",1],ID[\"EPSG\",8826]],PARAMETER[\"Northing at false" +
        "origin\",0,LENGTHUNIT[\"metre\",1],ID[\"EPSG\",8827]]],CS[" +
        "Cartesian,2],AXIS[\"easting (X)\",east,ORDER[1],LENGTHUNIT" +
        "[\"metre\",1]],AXIS[\"northing (Y)\",north,ORDER[2],LENGTHUNIT" +
        "[\"metre\",1]],USAGE[SCOPE[\"Engineering survey, topographic" +
        "mapping.\"],AREA[\"United States (USA) - North Carolina -" +
        "counties of Alamance; Alexander; Alleghany; Anson; Ashe; Avery; " +
        "Beaufort; Bertie; Bladen; Brunswick; Buncombe; Burke; Cabarrus; " +
        "Caldwell; Camden; Carteret; Caswell; Catawba; Chatham; Cherokee; " +
        "Chowan; Clay; Cleveland; Columbus; Craven; Cumberland; Currituck; " +
        "Dare; Davidson; Davie; Duplin; Durham; Edgecombe; Forsyth; " +
        "Franklin; Gaston; Gates; Graham; Granville; Greene; Guilford; " +
        "Halifax; Harnett; Haywood; Henderson; Hertford; Hoke; Hyde; " +
        "Iredell; Jackson; Johnston; Jones; Lee; Lenoir; Lincoln; Macon; " +
        "Madison; Martin; McDowell; Mecklenburg; Mitchell; Montgomery; " +
        "Moore; Nash; New Hanover; Northampton; Onslow; Orange; Pamlico; " +
        "Pasquotank; Pender; Perquimans; Person; Pitt; Polk; Randolph; " +
        "Richmond; Robeson; Rockingham; Rowan; Rutherford; Sampson; " +
        "Scotland; Stanly; Stokes; Surry; Swain; Transylvania; Tyrrell; " +
        "Union; Vance; Wake; Warren; Washington; Watauga; Wayne; Wilkes; " +
        "Wilson; Yadkin; Yancey.\"],BBOX[33.83,-84.33,36.59,-75.38]]," +
        "ID[\"EPSG\",3358]]\n",
        "region": {
            "b": 0,
            "cells": 1,
            "cells3": 1,
            "cols": 1,
            "cols3": 1,
            "depths": 1,
            "e": 1,
            "ewres": 1,
            "ewres3": 1,
            "n": 1,
            "nsres": 1,
            "nsres3": 1,
            "projection": 99,
            "rows": 1,
            "rows3": 1,
            "s": 0,
            "t": 1,
            "tbres": 1,
            "w": 0,
            "zone": 0
        }
    },
    "progress": {
        "num_of_steps": 2,
        "step": 2
    },
    "resource_id": "resource_id-a5b61779-ee68-426b-b3ed-991aaf24b980",
    "status": "finished",
    "time_delta": 0.20337486267089844,
    "timestamp": 1654755163.698429,
    "urls": {
        "resources": [],
        "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/" +
              "testuser/resource_id-a5b61779-ee68-426b-b3ed-991aaf24b980"
    },
    "user_id": "testuser"
}
