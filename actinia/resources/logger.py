#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2023 mundialis GmbH & Co. KG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

Template loader file
"""

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2023 mundialis GmbH & Co. KG"
__maintainer__ = "mundialis GmbH & Co. KG"


import logging
import os

# check if colorlog is installed
try:
    from colorlog import ColoredFormatter, StreamHandler

    log = logging.getLogger(__name__)
    formatter = ColoredFormatter(
        "%(log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            "DEBUG": "cyan",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
        secondary_log_colors={},
        style="%",
    )
    handler = StreamHandler()
    handler.setFormatter(formatter)
    log.addHandler(handler)
    log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
except Exception:
    logging.basicConfig(format="%(message)s")
    log = logging.getLogger(__name__)
    log.setLevel(os.environ.get("LOGLEVEL", "INFO"))
    log.debug("For colored logs install 'colorlog'")
