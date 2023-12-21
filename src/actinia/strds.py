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


from actinia.resources.logger import log


class Strds:
    # TODO init

    # TODO /locations/{location_name}/mapsets/{mapset_name}/strds/{strds_name}
    #                - GET
    def get_info(self):
        log.warning("Method not yes implemented")

    # TODO /locations/{location_name}/mapsets/{mapset_name}/strds/{strds_name}/
    #           raster_layers - PUT
    def register_rasters(self, name, start_time, end_time):
        log.warning("Method not yes implemented")

    # TODO /locations/{location_name}/mapsets/{mapset_name}/strds/{strds_name}/
    #           raster_layers - DELETE
    def unregister_rasters(self, names):
        log.warning("Method not yes implemented")

    # TODO /locations/{location_name}/mapsets/{mapset_name}/strds/{strds_name}/
    #           raster_layers - GET
    def get_rasters(self, names):
        log.warning("Method not yes implemented")

    # TODO /locations/{location_name}/mapsets/{mapset_name}/strds/{strds_name}/
    #           render - GET
    def render_in_single_image(
            self, n, s, e, w, start_time, end_time, width= 800 height=600
        ):
        log.warning("Method not yes implemented")
