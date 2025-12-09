#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# SPDX-FileCopyrightText: (c) 2022 mundialis GmbH & Co. KG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#######

__license__ = "GPL-3.0-or-later"
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
