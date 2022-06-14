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


class Region:
    def __init__(
        self,
        zone,
        projection,
        n,
        s,
        e,
        w,
        t,
        b,
        nsres,
        ewres,
        nsres3,
        ewres3,
        tbres,
        rows,
        cols,
        rows3,
        cols3,
        depths,
        cells,
        cells3,
    ):
        self.zone = zone
        self.projection = projection
        self.n = n
        self.s = s
        self.e = e
        self.w = w
        self.t = t
        self.b = b
        self.nsres = nsres
        self.ewres = ewres
        self.nsres3 = nsres3
        self.ewres3 = ewres3
        self.tbres = tbres
        self.rows = rows
        self.cols = cols
        self.rows3 = rows3
        self.cols3 = cols3
        self.depths = depths
        self.cells = cells
        self.cells3 = cells3
