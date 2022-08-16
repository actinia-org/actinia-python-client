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

get_vectors_mock = {
    "accept_datetime": "2022-06-14 09:57:39.460876",
    "accept_timestamp": 1655200659.4608743,
    "api_info": {
        "endpoint": "vectorlayersresource",
        "method": "GET",
        "path": f"/api/{ACTINIA_VERSION}/locations/nc_spm_08/mapsets/PERMANENT"
                "/vector_layers",
        "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/"
                       "nc_spm_08/mapsets/PERMANENT/vector_layers",
    },
    "datetime": "2022-06-14 09:57:39.817329",
    "http_code": 200,
    "message": "Processing successfully finished",
    "process_chain_list": [
        {
            "1": {
                "inputs": {"mapset": "PERMANENT", "type": "vector"},
                "module": "g.list",
            }
        }
    ],
    "process_log": [
        {
            "executable": "g.list",
            "id": "1",
            "parameter": ["mapset=PERMANENT", "type=vector"],
            "return_code": 0,
            "run_time": 0.10045146942138672,
            "stderr": [""],
            "stdout": "P079214\nP079215\nP079218\nP079219\nboundary_county\n"
            "boundary_municp\nbridges\nbusroute1\nbusroute11\nbusroute6\n"
            "busroute_a\nbusroutesall\nbusstopsall\ncensus_wake2000\n"
            "censusblk_swwake\ncomm_colleges\nelev_lid792_bepts\nelev_lid792"
            "_cont1m\nelev_lid792_randpts\nelev_lidrural_mrpts\nelev_lidrural"
            "_mrptsft\nelev_ned10m_cont10m\nfirestations\ngeodetic_pts\n"
            "geodetic_swwake_pts\ngeology\ngeonames_NC\ngeonames_wake\n"
            "hospitals\nlakes\nnc_state\noverpasses\npoi_names_wake\n"
            "precip_30ynormals\nprecip_30ynormals_3d\nrailroads\nroadsmajor"
            "\nschools_wake\nsoils_general\nsoils_wake\nstreams\nstreets_wake"
            "\nswwake_10m\nurbanarea\nusgsgages\nzipcodes_wake\n",
        }
    ],
    "process_results": [
        "P079214",
        "P079215",
        "P079218",
        "P079219",
        "boundary_county",
        "boundary_municp",
        "bridges",
        "busroute1",
        "busroute11",
        "busroute6",
        "busroute_a",
        "busroutesall",
        "busstopsall",
        "census_wake2000",
        "censusblk_swwake",
        "comm_colleges",
        "elev_lid792_bepts",
        "elev_lid792_cont1m",
        "elev_lid792_randpts",
        "elev_lidrural_mrpts",
        "elev_lidrural_mrptsft",
        "elev_ned10m_cont10m",
        "firestations",
        "geodetic_pts",
        "geodetic_swwake_pts",
        "geology",
        "geonames_NC",
        "geonames_wake",
        "hospitals",
        "lakes",
        "nc_state",
        "overpasses",
        "poi_names_wake",
        "precip_30ynormals",
        "precip_30ynormals_3d",
        "railroads",
        "roadsmajor",
        "schools_wake",
        "soils_general",
        "soils_wake",
        "streams",
        "streets_wake",
        "swwake_10m",
        "urbanarea",
        "usgsgages",
        "zipcodes_wake",
    ],
    "progress": {"num_of_steps": 1, "step": 1},
    "resource_id": "resource_id-2a958ad5-020c-4b3a-a748-d43e11698914",
    "status": "finished",
    "time_delta": 0.35648655891418457,
    "timestamp": 1655200659.8172982,
    "urls": {
        "resources": [],
        "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser"
                  "/resource_id-2a958ad5-020c-4b3a-a748-d43e11698914",
    },
    "user_id": "testuser",
}

vector_info_resp = {
    "Attributes": [
        {"column": "cat", "type": "INTEGER"},
        {"column": "AREA", "type": "DOUBLE PRECISION"},
        {"column": "PERIMETER", "type": "DOUBLE PRECISION"},
        {"column": "FIPS", "type": "DOUBLE PRECISION"},
        {"column": "NAME", "type": "CHARACTER"},
        {"column": "NAME_LOCAS", "type": "CHARACTER"},
        {"column": "DOT_DISTRI", "type": "INTEGER"},
        {"column": "DOT_DIVISI", "type": "INTEGER"},
        {"column": "DOT_COUNTY", "type": "INTEGER"},
        {"column": "COUNTY_100", "type": "INTEGER"},
        {"column": "DOT_GROUP_", "type": "CHARACTER"},
        {"column": "ACRES", "type": "DOUBLE PRECISION"},
        {"column": "ABBR_5CHAR", "type": "CHARACTER"},
        {"column": "ABBR_4CHAR", "type": "CHARACTER"},
        {"column": "ABBR_2CHAR", "type": "CHARACTER"},
        {"column": "Z_MEAN", "type": "DOUBLE PRECISION"},
        {"column": "Z_MIN", "type": "DOUBLE PRECISION"},
        {"column": "Z_MAX", "type": "DOUBLE PRECISION"},
        {"column": "Z_ZONE", "type": "DOUBLE PRECISION"},
        {"column": "CO_CENSUS", "type": "CHARACTER"},
        {"column": "DIV_CONTAC", "type": "CHARACTER"},
        {"column": "DIST_CONTA", "type": "CHARACTER"},
        {"column": "CO_WIKIPED", "type": "CHARACTER"},
        {"column": "Shape_Leng", "type": "DOUBLE PRECISION"},
        {"column": "Shape_Area", "type": "DOUBLE PRECISION"},
    ],
    "COMMAND": ' v.db.connect -o map="boundary_county@PERMANENT" driver='
               '"sqlite" database="$GISDBASE/$LOCATION_NAME/$MAPSET/sqlite/'
               'sqlite.db" table="boundary_county" key="cat" layer="1" '
               'separator="|"',
    "areas": "926",
    "attribute_database": "/actinia_core/workspace/temp_db/gisdbase_6e4ca293"
                          "5544442e9b68954aae25f809/nc_spm_08/PERMANENT/sqlite"
                          "/sqlite.db",
    "attribute_database_driver": "sqlite",
    "attribute_layer_name": "boundary_county",
    "attribute_layer_number": "1",
    "attribute_primary_key": "cat",
    "attribute_table": "boundary_county",
    "bottom": "0.000000",
    "boundaries": "1910",
    "centroids": "926",
    "comment": "",
    "creator": "helena",
    "database": "/actinia_core/workspace/temp_db/gisdbase_6e4ca2935544442e9b6"
                "8954aae25f809",
    "digitization_threshold": "0.000000",
    "east": "962679.95935005",
    "format": "native",
    "islands": "130",
    "level": "2",
    "lines": "0",
    "location": "nc_spm_08",
    "map3d": "0",
    "mapset": "PERMANENT",
    "name": "boundary_county",
    "nodes": "1114",
    "north": "318097.688745074",
    "num_dblinks": "1",
    "organization": "NC OneMap",
    "points": "0",
    "primitives": "2836",
    "projection": "Lambert Conformal Conic",
    "scale": "1:1",
    "source_date": "Tue Apr  3 13:23:49 2007",
    "south": "-15865.3468644768",
    "timestamp": "none",
    "title": "North Carolina county boundaries (polygon map)",
    "top": "0.000000",
    "west": "124002.67019024",
}

get_vector_info_mock = {
    "accept_datetime": "2022-06-14 09:58:37.867650",
    "accept_timestamp": 1655200717.8676484,
    "api_info": {
        "endpoint": "vectorlayerresource",
        "method": "GET",
        "path": f"/api/{ACTINIA_VERSION}/locations/nc_spm_08/mapsets/PERMANENT"
                "/vector_layers/boundary_county",
        "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/"
                       "nc_spm_08/mapsets/PERMANENT/vector_layers/"
                       "boundary_county",
    },
    "datetime": "2022-06-14 09:58:39.624698",
    "http_code": 200,
    "message": "Processing successfully finished",
    "process_chain_list": [
        {
            "1": {
                "flags": "gte",
                "inputs": {"map": "boundary_county@PERMANENT"},
                "module": "v.info",
            },
            "2": {
                "flags": "h",
                "inputs": {"map": "boundary_county@PERMANENT"},
                "module": "v.info",
            },
            "3": {
                "flags": "c",
                "inputs": {"map": "boundary_county@PERMANENT"},
                "module": "v.info",
            },
        }
    ],
    "process_log": [
        {
            "executable": "v.info",
            "id": "1",
            "mapset_size": 421,
            "parameter": ["map=boundary_county@PERMANENT", "-gte"],
            "return_code": 0,
            "run_time": 0.30083537101745605,
            "stderr": [""],
            "stdout": "name=boundary_county\nmapset=PERMANENT\nlocation="
                      "nc_spm_08\ndatabase=/actinia_core/workspace/temp_db/"
                      "gisdbase_6e4ca2935544442e9b68954aae25f809\ntitle=North "
                      "Carolina county boundaries (polygon map)\nscale=1:1\n"
                      "creator=helena\norganization=NC OneMap\nsource_date="
                      "Tue Apr  3 13:23:49 2007\ntimestamp=none\nformat=native"
                      "\nlevel=2\nnum_dblinks=1\nattribute_layer_number=1\n"
                      "attribute_layer_name=boundary_county\nattribute_"
                      "database=/actinia_core/workspace/temp_db/gisdbase_6e4ca"
                      "2935544442e9b68954aae25f809/nc_spm_08/PERMANENT/sqlite/"
                      "sqlite.db\nattribute_database_driver=sqlite\nattribute"
                      "_table=boundary_county\nattribute_primary_key=cat\n"
                      "projection=Lambert Conformal Conic\ndigitization_thres"
                      "hold=0.000000\ncomment=\nnorth=318097.688745074\nsouth"
                      "=-15865.3468644768\neast=962679.95935005\nwest=124002."
                      "67019024\ntop=0.000000\nbottom=0.000000\nnodes=1114\n"
                      "points=0\nlines=0\nboundaries=1910\ncentroids=926\n"
                      "areas=926\nislands=130\nprimitives=2836\nmap3d=0\n",
        },
        {
            "executable": "v.info",
            "id": "2",
            "mapset_size": 421,
            "parameter": ["map=boundary_county@PERMANENT", "-h"],
            "return_code": 0,
            "run_time": 0.20082664489746094,
            "stderr": [""],
            "stdout": 'COMMAND: v.in.ogr dsn="CountyBoundaryShoreline.shp" '
                      'output="boundary_county" min_area=0.0001 snap=-1\nGISD'
                      'BASE: /bigdata/bakncgrassdata\nLOCATION: nc_spm_03 '
                      'MAPSET: user1 USER: helena DATE: Tue Apr  3 13:23:49 '
                      '2007\n-------------------------------------------------'
                      '--------------------------------\n926 input polygons\n'
                      'total area: 1.541189e+11 (926 areas)\noverlapping area:'
                      ' 0.000000e+00 (0 areas)\narea without category: '
                      '0.000000e+00 (0 areas)\n-------------------------------'
                      '--------------------------------------------------\n---'
                      '-------------------------------------------------------'
                      '-----------------------\nCOMMAND: v.db.connect -o map='
                      '"boundary_county@PERMANENT" driver="sqlite" database='
                      '"/home/neteler/grassdata/nc_spm_latest/nc_spm_08/'
                      'PERMANENT/sqlite/sqlite.db" table="boundary_county" '
                      'key="cat" layer="1" separator="|"\nGISDBASE: /home/'
                      'neteler/grassdata/nc_spm_latest\nLOCATION: nc_spm_08 '
                      'MAPSET: PERMANENT USER: neteler DATE: Mon Nov 26 16:55:'
                      '29 2012\n----------------------------------------------'
                      '-----------------------------------\nCOMMAND: '
                      'v.db.connect -o map="boundary_county@PERMANENT" driver='
                      '"sqlite" database="$GISDBASE/$LOCATION_NAME/$MAPSET/'
                      'sqlite/sqlite.db" table="boundary_county" key="cat" '
                      'layer="1" separator="|"\nGISDBASE: /home/neteler/'
                      'grassdata\nLOCATION: nc_spm_08_grass7 MAPSET: PERMANENT'
                      ' USER: neteler DATE: Fri Dec  7 23:25:11 2012\n',
        },
        {
            "executable": "v.info",
            "id": "3",
            "mapset_size": 421,
            "parameter": ["map=boundary_county@PERMANENT", "-c"],
            "return_code": 0,
            "run_time": 0.2508242130279541,
            "stderr": [
                "Displaying column types/names for database connection of "
                "layer <1>:",
                "",
            ],
            "stdout": "INTEGER|cat\nDOUBLE PRECISION|AREA\nDOUBLE PRECISION|"
                      "PERIMETER\nDOUBLE PRECISION|FIPS\nCHARACTER|NAME\n"
                      "CHARACTER|NAME_LOCAS\nINTEGER|DOT_DISTRI\nINTEGER|"
                      "DOT_DIVISI\nINTEGER|DOT_COUNTY\nINTEGER|COUNTY_100\n"
                      "CHARACTER|DOT_GROUP_\nDOUBLE PRECISION|ACRES\nCHARACTER"
                      "|ABBR_5CHAR\nCHARACTER|ABBR_4CHAR\nCHARACTER|"
                      "ABBR_2CHAR\nDOUBLE PRECISION|Z_MEAN\nDOUBLE PRECISION|"
                      "Z_MIN\nDOUBLE PRECISION|Z_MAX\nDOUBLE PRECISION|Z_ZONE"
                      "\nCHARACTER|CO_CENSUS\nCHARACTER|DIV_CONTAC\nCHARACTER"
                      "|DIST_CONTA\nCHARACTER|CO_WIKIPED\nDOUBLE PRECISION|"
                      "Shape_Leng\nDOUBLE PRECISION|Shape_Area\n",
        },
    ],
    "process_results": vector_info_resp,
    "progress": {"num_of_steps": 3, "step": 3},
    "resource_id": "resource_id-dc63156b-edf8-4295-a1af-4c149f847730",
    "status": "finished",
    "time_delta": 1.757124423980713,
    "timestamp": 1655200719.6246197,
    "urls": {
        "resources": [],
        "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser"
                  "/resource_id-dc63156b-edf8-4295-a1af-4c149f847730",
    },
    "user_id": "testuser",
}

upload_vector_resp = {
    "accept_datetime": "2022-06-14 10:00:30.093043",
    "accept_timestamp": 1655200830.0930417,
    "api_info": {
        "endpoint": "vectorlayerresource",
        "method": "POST",
        "path": f"/api/{ACTINIA_VERSION}/locations/nc_spm_08/mapsets/"
                "raster_upload/vector_layers/test_vector",
        "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/"
                       "nc_spm_08/mapsets/raster_upload/vector_layers/"
                       "test_vector",
    },
    "datetime": "2022-06-14 10:00:35.041458",
    "http_code": 200,
    "message": "Vector layer <test_vector> successfully imported.",
    "process_chain_list": [
        {
            "1": {
                "inputs": {
                    "mapset": "raster_upload",
                    "pattern": "test_vector",
                    "type": "vector",
                },
                "module": "g.list",
            }
        },
        {
            "1": {
                "inputs": {
                    "input": "/actinia_core/workspace/download_cache/testuser/"
                             "unzip_afbddb40-e370-4c7d-b00c-4823f0853d82/"
                             "firestations.shp"
                },
                "module": "v.import",
                "outputs": {"output": {"name": "test_vector"}},
            }
        },
    ],
    "process_log": [
        {
            "executable": "g.list",
            "id": "1",
            "mapset_size": 489,
            "parameter": [
                "type=vector",
                "pattern=test_vector",
                "mapset=raster_upload",
            ],
            "return_code": 0,
            "run_time": 0.10049247741699219,
            "stderr": [""],
            "stdout": "",
        },
        {
            "executable": "v.import",
            "id": "1",
            "mapset_size": 33790,
            "parameter": [
                "input=/actinia_core/workspace/download_cache/testuser/"
                "unzip_afbddb40-e370-4c7d-b00c-4823f0853d82/firestations.shp",
                "output=test_vector",
            ],
            "return_code": 0,
            "run_time": 1.1054775714874268,
            "stderr": [
                "Check if OGR layer <firestations> contains polygons...",
                "0..2..4..7..9..11..14..16..18..21..23..25..28..30..32..35.."
                "38..40..42..45..47..49..52..54..56..59..61..63..66..69..71.."
                "73..76..78..80..83..85..87..90..92..94..97..100",
                "Creating attribute table for layer <firestations>...",
                "Column name <cat> renamed to <cat_>",
                "Importing 71 features (OGR layer <firestations>)...",
                "0..2..4..7..9..11..14..16..18..21..23..25..28..30..32..35.."
                "38..40..42..45..47..49..52..54..56..59..61..63..66..69..71.."
                "73..76..78..80..83..85..87..90..92..94..97..100",
                "-----------------------------------------------------",
                "Building topology for vector map <test_vector@mapset_"
                "128b8e67969648d38aee49c2ac0a8f28>...",
                "Registering primitives...",
                "",
                "Input </actinia_core/workspace/download_cache/testuser/unzip"
                "_afbddb40-e370-4c7d-b00c-4823f0853d82/firestations.shp> "
                "successfully imported without reprojection",
                "",
            ],
            "stdout": "",
        },
    ],
    "process_results": {},
    "progress": {"num_of_steps": 2, "step": 2},
    "resource_id": "resource_id-f887fddc-ca92-4e6b-aaaa-169023627567",
    "status": "finished",
    "time_delta": 4.9484381675720215,
    "timestamp": 1655200835.041446,
    "urls": {
        "resources": [],
        "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser"
                  "/resource_id-f887fddc-ca92-4e6b-aaaa-169023627567",
    },
    "user_id": "testuser",
}

start_job_resp = {
    "accept_datetime": "2022-06-14 10:00:30.093043",
    "accept_timestamp": 1655200830.0930417,
    "api_info": {
        "endpoint": "vectorlayerresource",
        "method": "POST",
        "path": f"/api/{ACTINIA_VERSION}/locations/nc_spm_08/mapsets/raster_"
                "upload/vector_layers/test_vector",
        "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/"
                       "nc_spm_08/mapsets/raster_upload/vector_layers/"
                       "test_vector",
    },
    "datetime": "2022-06-14 10:00:30.098413",
    "http_code": 200,
    "message": "Resource accepted",
    "process_chain_list": [],
    "process_results": {},
    "resource_id": "resource_id-f887fddc-ca92-4e6b-aaaa-169023627567",
    "status": "accepted",
    "time_delta": 0.005391836166381836,
    "timestamp": 1655200830.0984113,
    "urls": {
        "resources": [],
        "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser"
                  "/resource_id-f887fddc-ca92-4e6b-aaaa-169023627567",
    },
    "user_id": "testuser",
}

delete_vector_resp = {
    "accept_datetime": "2022-06-14 10:03:56.402405",
    "accept_timestamp": 1655201036.402403,
    "api_info": {
        "endpoint": "vectorlayerresource",
        "method": "DELETE",
        "path": f"/api/{ACTINIA_VERSION}/locations/nc_spm_08/mapsets/"
                "raster_upload/vector_layers/test_vector",
        "request_url": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/"
                       "nc_spm_08/mapsets/raster_upload/vector_layers/"
                       "test_vector",
    },
    "datetime": "2022-06-14 10:03:56.981348",
    "http_code": 200,
    "message": "Vector layer <test_vector> successfully removed.",
    "process_chain_list": [
        {
            "1": {
                "flags": "f",
                "inputs": {"name": "test_vector", "type": "vector"},
                "module": "g.remove",
            }
        }
    ],
    "process_log": [
        {
            "executable": "g.remove",
            "id": "1",
            "parameter": ["type=vector", "name=test_vector", "-f"],
            "return_code": 0,
            "run_time": 0.4009582996368408,
            "stderr": ["Removing vector <test_vector>", ""],
            "stdout": "",
        }
    ],
    "process_results": {},
    "progress": {"num_of_steps": 1, "step": 1},
    "resource_id": "resource_id-c4713ee6-4aad-4831-9d55-ad2c989937da",
    "status": "finished",
    "time_delta": 0.5789728164672852,
    "timestamp": 1655201036.9813201,
    "urls": {
        "resources": [],
        "status": f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser"
                  "/resource_id-c4713ee6-4aad-4831-9d55-ad2c989937da",
    },
    "user_id": "testuser",
}
