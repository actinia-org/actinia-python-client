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

import json
import requests


def request_and_check(url, auth, status_code=200):
    """Function to send a GET request to an URL and check the status code.

    Parameters:
        url (string): URL as string
        auth (tuple): Tupel of user and password
        status_code (int): Status code to check if it is set; default is 200

    Returns:
        (dict): returns text of the response as dictionary

    Throws an error if the request does not have the status_code
    """
    resp = requests.get(url, auth=auth)
    if resp.status_code != status_code:
        raise Exception(f"Error {resp.status_code}: {resp.text}")
    return json.loads(resp.text)
