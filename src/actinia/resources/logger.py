#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2023 mundialis GmbH & Co. KG

SPDX-License-Identifier: GPL-3.0-or-later

Template loader file
"""

__license__ = "GPL-3.0-or-later"
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
