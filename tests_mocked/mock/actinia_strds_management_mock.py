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
__maintainer__ = "testuser Weinmann"

from .actinia_mock import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
)

get_strds_mock = {
    'accept_datetime': '2022-06-17 15:37:38.042299',
    'accept_timestamp': 1655480258.0422983,
    'api_info': {
        'endpoint': 'syncstrdslisterresource',
        'method': 'GET',
        'path': '/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds',
        'request_url': 'http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds'
    },
    'datetime': '2022-06-17 15:37:38.783924',
    'http_code': 200,
    'message': 'Processing successfully finished',
    'process_chain_list': [{
        'list': [{
            'id': 'list_strds_648edc50300d4229ab40d302d2aa3010',
            'inputs': [{
                'param': 'type',
                'value': 'strds'
            }, {
                'param': 'column',
                'value': 'name'
            }, {
                'param': 'where',
                'value': "mapset='modis_lst'"
            }],
            'module': 't.list'
        }],
        'version': 1
    }],
    'process_log': [{
        'executable': 't.list',
        'id': 'list_strds_648edc50300d4229ab40d302d2aa3010',
        'parameter': ['type=strds', 'column=name', "where=mapset='modis_lst'"],
        'return_code': 0,
        'run_time': 0.6035289764404297,
        'stderr': ['WARNING: Temporal database version mismatch detected.', 'Run t.upgrade command to upgrade your temporal database.', 'Consider creating a backup of your temporal database to avoid loosing data in case something goes wrong.', 'Supported temporal database version is: 3', 'Your existing temporal database version: 2', 'Current temporal database info: ', 'DBMI interface:..... sqlite3', 'Temporal database:.. /actinia_core/workspace/temp_db/gisdbase_648edc50300d4229ab40d302d2aa3010/nc_spm_08/modis_lst/tgis/sqlite.db', '----------------------------------------------', 'Space time raster datasets with absolute time available in mapset <modis_lst>:', ''],
        'stdout': 'LST_Day_monthly\n'
    }],
    'process_results': ['LST_Day_monthly'],
    'progress': {
        'num_of_steps': 1,
        'step': 1
    },
    'resource_id': 'resource_id-823ea9a1-355e-4422-b985-fbed561c9150',
    'status': 'finished',
    'time_delta': 0.7416486740112305,
    'timestamp': 1655480258.7839065,
    'urls': {
        'resources': [],
        'status': 'http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-823ea9a1-355e-4422-b985-fbed561c9150'
    },
    'user_id': 'actinia-gdi'
}

strds_info_resp = {
    'aggregation_type': 'None',
    'bottom': '0.0',
    'creation_time': "'2019-09-02 13:03:42.173278'",
    'creator': 'mneteler',
    'east': '1550934.464115',
    'end_time': "'2017-01-01 00:00:00'",
    'ewres_max': '5600.0',
    'ewres_min': '5600.0',
    'granularity': "'1 month'",
    'id': 'LST_Day_monthly@modis_lst',
    'map_time': 'interval',
    'mapset': 'modis_lst',
    'max_max': '15650.0',
    'max_min': '14360.0',
    'min_max': '14714.0',
    'min_min': '12950.0',
    'modification_time': "'2019-09-02 13:04:01.703962'",
    'name': 'LST_Day_monthly',
    'north': '760180.124115',
    'nsres_max': '5600.0',
    'nsres_min': '5600.0',
    'number_of_maps': '24',
    'number_of_semantic_labels': 'None',
    'raster_register': 'raster_map_register_78a1d5e30c904a5db2d15b939b5b0a3b',
    'semantic_labels': 'None',
    'semantic_type': 'mean',
    'south': '-415819.875885',
    'start_time': "'2015-01-01 00:00:00'",
    'temporal_type': 'absolute',
    'top': '0.0',
    'west': '-448265.535885'
}

get_strds_info_mock = {
    'accept_datetime': '2022-06-17 15:40:16.856744',
    'accept_timestamp': 1655480416.856744,
    'api_info': {
        'endpoint': 'strdsmanagementresource',
        'method': 'GET',
        'path': '/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly',
        'request_url': 'http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/modis_lst/strds/LST_Day_monthly'
    },
    'datetime': '2022-06-17 15:40:17.595795',
    'http_code': 200,
    'message': 'Information gathering for STRDS <LST_Day_monthly> successful',
    'process_chain_list': [{
        'list': [{
            'flags': 'g',
            'id': 'strds_info_76093b4d8371438a91f50a5932be84c4',
            'inputs': [{
                'param': 'type',
                'value': 'strds'
            }, {
                'param': 'input',
                'value': 'LST_Day_monthly'
            }],
            'module': 't.info'
        }],
        'version': 1
    }],
    'process_log': [{
        'executable': 't.info',
        'id': 'strds_info_76093b4d8371438a91f50a5932be84c4',
        'parameter': ['type=strds', 'input=LST_Day_monthly', '-g'],
        'return_code': 0,
        'run_time': 0.603538990020752,
        'stderr': ['WARNING: Temporal database version mismatch detected.', 'Run t.upgrade command to upgrade your temporal database.', 'Consider creating a backup of your temporal database to avoid loosing data in case something goes wrong.', 'Supported temporal database version is: 3', 'Your existing temporal database version: 2', 'Current temporal database info: ', 'DBMI interface:..... sqlite3', 'Temporal database:.. /actinia_core/workspace/temp_db/gisdbase_76093b4d8371438a91f50a5932be84c4/nc_spm_08/modis_lst/tgis/sqlite.db', ''],
        'stdout': "id=LST_Day_monthly@modis_lst\nname=LST_Day_monthly\nmapset=modis_lst\ncreator=mneteler\ntemporal_type=absolute\ncreation_time='2019-09-02 13:03:42.173278'\nmodification_time='2019-09-02 13:04:01.703962'\nsemantic_type=mean\nstart_time='2015-01-01 00:00:00'\nend_time='2017-01-01 00:00:00'\ngranularity='1 month'\nmap_time=interval\nnorth=760180.124115\nsouth=-415819.875885\neast=1550934.464115\nwest=-448265.535885\ntop=0.0\nbottom=0.0\nraster_register=raster_map_register_78a1d5e30c904a5db2d15b939b5b0a3b\nnsres_min=5600.0\nnsres_max=5600.0\newres_min=5600.0\newres_max=5600.0\nmin_min=12950.0\nmin_max=14714.0\nmax_min=14360.0\nmax_max=15650.0\naggregation_type=None\nnumber_of_semantic_labels=None\nsemantic_labels=None\nnumber_of_maps=24\n"
    }],
    'process_results': strds_info_resp,
    'progress': {
        'num_of_steps': 1,
        'step': 1
    },
    'resource_id': 'resource_id-e772955a-2077-4beb-8730-70c6558d9f8d',
    'status': 'finished',
    'time_delta': 0.7390720844268799,
    'timestamp': 1655480417.5957785,
    'urls': {
        'resources': [],
        'status': 'http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-e772955a-2077-4beb-8730-70c6558d9f8d'
    },
    'user_id': 'actinia-gdi'
}

create_strds_resp = {
  "accept_datetime": "2022-06-17 15:45:44.766312",
  "accept_timestamp": 1655480744.766312,
  "api_info": {
    "endpoint": "strdsmanagementresource",
    "method": "POST",
    "path": "/api/v3/locations/nc_spm_08/mapsets/raster_test_mapset/strds/test_strds",
    "request_url": "http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/raster_test_mapset/strds/test_strds"
  },
  "datetime": "2022-06-17 15:45:46.111688",
  "http_code": 200,
  "message": "STRDS <test_strds> successfully created",
  "process_chain_list": [
    {
      "list": [
        {
          "id": "list_strds_683588ef644e4aecbcd53b38bcca6966",
          "inputs": [
            {
              "param": "type",
              "value": "strds"
            },
            {
              "param": "where",
              "value": "id = 'test_strds@raster_test_mapset'"
            }
          ],
          "module": "t.list"
        }
      ],
      "version": 1
    },
    {
      "list": [
        {
          "id": "create_strds_683588ef644e4aecbcd53b38bcca6966",
          "inputs": [
            {
              "param": "type",
              "value": "strds"
            },
            {
              "param": "title",
              "value": "title"
            },
            {
              "param": "description",
              "value": "description"
            }
          ],
          "module": "t.create",
          "outputs": [
            {
              "param": "output",
              "value": "test_strds"
            }
          ]
        }
      ],
      "version": 1
    }
  ],
  "process_log": [
    {
      "executable": "t.list",
      "id": "list_strds_683588ef644e4aecbcd53b38bcca6966",
      "parameter": [
        "type=strds",
        "where=id = 'test_strds@raster_test_mapset'"
      ],
      "return_code": 0,
      "run_time": 0.6032302379608154,
      "stderr": [
        "----------------------------------------------",
        ""
      ],
      "stdout": ""
    },
    {
      "executable": "t.create",
      "id": "create_strds_683588ef644e4aecbcd53b38bcca6966",
      "parameter": [
        "type=strds",
        "title=title",
        "description=description",
        "output=test_strds"
      ],
      "return_code": 0,
      "run_time": 0.6031455993652344,
      "stderr": [
        ""
      ],
      "stdout": ""
    }
  ],
  "process_results": {},
  "progress": {
    "num_of_steps": 2,
    "step": 2
  },
  "resource_id": "resource_id-8934672c-1009-486f-9875-bcdfb7dde452",
  "status": "finished",
  "time_delta": 1.3453986644744873,
  "timestamp": 1655480746.1116722,
  "urls": {
    "resources": [],
    "status": "http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-8934672c-1009-486f-9875-bcdfb7dde452"
  },
  "user_id": "actinia-gdi"
}

add_raster_to_strds = {
  "accept_datetime": "2022-06-17 15:46:44.960394",
  "accept_timestamp": 1655480804.960393,
  "api_info": {
    "endpoint": "strdsrastermanagement",
    "method": "PUT",
    "path": "/api/v3/locations/nc_spm_08/mapsets/raster_test_mapset/strds/test_strds/raster_layers",
    "request_url": "http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/raster_test_mapset/strds/test_strds/raster_layers"
  },
  "datetime": "2022-06-17 15:46:45.638150",
  "http_code": 200,
  "message": "Processing successfully finished",
  "process_chain_list": [
    {
      "1": {
        "inputs": {
          "file": "/actinia_core/workspace/temp_db/gisdbase_a008b051faab49fda97ce8cfb330053f/.tmp/tmpwtxaaz6j",
          "input": "test_strds@raster_test_mapset",
          "separator": "|",
          "type": "raster"
        },
        "module": "t.register"
      }
    }
  ],
  "process_log": [
    {
      "executable": "t.register",
      "id": "1",
      "parameter": [
        "input=test_strds@raster_test_mapset",
        "type=raster",
        "separator=|",
        "file=/actinia_core/workspace/temp_db/gisdbase_a008b051faab49fda97ce8cfb330053f/.tmp/tmpwtxaaz6j"
      ],
      "return_code": 0,
      "run_time": 0.551997184753418,
      "stderr": [
        "0..100",
        "0..100",
        ""
      ],
      "stdout": ""
    }
  ],
  "process_results": {},
  "progress": {
    "num_of_steps": 1,
    "step": 1
  },
  "resource_id": "resource_id-f1c9abd1-b99d-42cc-8239-68baafee4eb5",
  "status": "finished",
  "time_delta": 0.6777949333190918,
  "timestamp": 1655480805.63812,
  "urls": {
    "resources": [],
    "status": "http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-f1c9abd1-b99d-42cc-8239-68baafee4eb5"
  },
  "user_id": "actinia-gdi"
}

remove_raster_layers_from_strds = {
  "accept_datetime": "2022-06-17 15:47:49.171113",
  "accept_timestamp": 1655480869.1711125,
  "api_info": {
    "endpoint": "strdsrastermanagement",
    "method": "DELETE",
    "path": "/api/v3/locations/nc_spm_08/mapsets/raster_test_mapset/strds/test_strds/raster_layers",
    "request_url": "http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/raster_test_mapset/strds/test_strds/raster_layers"
  },
  "datetime": "2022-06-17 15:47:50.182321",
  "http_code": 200,
  "message": "Raster maps <['test_layer_1']> successfully unregistered from test_strds",
  "process_chain_list": [
    {
      "list": [
        {
          "id": "strds_unregister_raster_3b9975162fe24edfbe9c5a8333c1502c",
          "inputs": [
            {
              "param": "input",
              "value": "test_strds"
            },
            {
              "param": "type",
              "value": "raster"
            },
            {
              "param": "maps",
              "value": "test_layer_1@raster_test_mapset"
            }
          ],
          "module": "t.unregister"
        }
      ],
      "version": 1
    }
  ],
  "process_log": [
    {
      "executable": "t.unregister",
      "id": "strds_unregister_raster_3b9975162fe24edfbe9c5a8333c1502c",
      "mapset_size": 492098,
      "parameter": [
        "input=test_strds",
        "type=raster",
        "maps=test_layer_1@raster_test_mapset"
      ],
      "return_code": 0,
      "run_time": 0.602849006652832,
      "stderr": [
        "Default TGIS driver / database set to:",
        "driver: sqlite",
        "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
        "Unregister maps",
        "0..100",
        "Unregister maps from space time dataset <test_strds>",
        ""
      ],
      "stdout": ""
    }
  ],
  "process_results": {},
  "progress": {
    "num_of_steps": 1,
    "step": 1
  },
  "resource_id": "resource_id-b9e3ffe1-1f58-4cd8-8998-5460ae44a28d",
  "status": "finished",
  "time_delta": 1.011221170425415,
  "timestamp": 1655480870.182317,
  "urls": {
    "resources": [],
    "status": "http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-b9e3ffe1-1f58-4cd8-8998-5460ae44a28d"
  },
  "user_id": "actinia-gdi"
}

delete_strds_resp = {
  "accept_datetime": "2022-06-17 15:49:06.374976",
  "accept_timestamp": 1655480946.3749757,
  "api_info": {
    "endpoint": "strdsmanagementresource",
    "method": "DELETE",
    "path": "/api/v3/locations/nc_spm_08/mapsets/raster_test_mapset/strds/test_strds",
    "request_url": "http://localhost:8088/api/v3/locations/nc_spm_08/mapsets/raster_test_mapset/strds/test_strds"
  },
  "datetime": "2022-06-17 15:49:07.402816",
  "http_code": 200,
  "message": "STRDS <test_strds> successfully deleted",
  "process_chain_list": [
    {
      "list": [
        {
          "flags": "f",
          "id": "remove_strds_31d05d5259474d7e910ccf5278a95a5c",
          "inputs": [
            {
              "param": "type",
              "value": "strds"
            },
            {
              "param": "inputs",
              "value": "test_strds"
            }
          ],
          "module": "t.remove"
        }
      ],
      "version": 1
    }
  ],
  "process_log": [
    {
      "executable": "t.remove",
      "id": "remove_strds_31d05d5259474d7e910ccf5278a95a5c",
      "mapset_size": 492098,
      "parameter": [
        "type=strds",
        "inputs=test_strds",
        "-f"
      ],
      "return_code": 0,
      "run_time": 0.6031880378723145,
      "stderr": [
        "Default TGIS driver / database set to:",
        "driver: sqlite",
        "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
        ""
      ],
      "stdout": ""
    }
  ],
  "process_results": {},
  "progress": {
    "num_of_steps": 1,
    "step": 1
  },
  "resource_id": "resource_id-e3ddde14-b733-456f-be8c-4d634e70841d",
  "status": "finished",
  "time_delta": 1.0278778076171875,
  "timestamp": 1655480947.402803,
  "urls": {
    "resources": [],
    "status": "http://localhost:8088/api/v3/resources/actinia-gdi/resource_id-e3ddde14-b733-456f-be8c-4d634e70841d"
  },
  "user_id": "actinia-gdi"
}
