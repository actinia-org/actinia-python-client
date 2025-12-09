#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
SPDX-FileCopyrightText: (c) 2023-2025 mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later

Template loader file
"""

__license__ = "GPL-3.0-or-later"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2023-2025 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH % Co. KG"


from jinja2 import Environment, PackageLoader

tplEnv = Environment(loader=PackageLoader("actinia", "templates"))
