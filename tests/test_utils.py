#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# Copyright (c) 2023 mundialis GmbH & Co. KG
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
__author__ = "Anika Weinmann, Markus Metz"
__copyright__ = "Copyright 2023, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import pytest

from actinia.utils import (
    create_actinia_pc_item,
    request_and_check,
    set_job_names,
)
from .actinia_config import ACTINIA_BASEURL, ACTINIA_VERSION, ACTINIA_AUTH


class TestActiniaUtils(object):
    def test_request_and_check(self):
        """Test request_and_check utils function."""
        url = f"{ACTINIA_BASEURL}api/{ACTINIA_VERSION}/version"
        resp = request_and_check(url, ACTINIA_AUTH, status_code=200)
        assert "version" in resp

    def test_request_and_check_wrong_url(self):
        """Test request_and_check utils function with ."""
        url = f"{ACTINIA_BASEURL}api/{ACTINIA_VERSION}/version_fail"
        err_msg = "The requested URL was not found on the server."
        with pytest.raises(Exception) as excinfo:
            request_and_check(url, ACTINIA_AUTH, status_code=200)
        assert err_msg in str(excinfo.value)

    def test_request_and_check_wrong_auth(self):
        """Test request_and_check utils function with wrong auth."""
        url = f"{ACTINIA_BASEURL}api/{ACTINIA_VERSION}/locations"
        err_msg = "Unauthorized Access"
        wrong_auth = ("actinia-gdi", "wrong_pw")
        with pytest.raises(Exception) as excinfo:
            request_and_check(url, wrong_auth, status_code=200)
        assert err_msg in str(excinfo.value)

    def test_set_job_names(self):
        """Test set_job_names utils function."""
        def_name = "def_job_name"
        name_to_set = "test"
        orig_name, name = set_job_names(name_to_set, default_name=def_name)
        assert name_to_set == orig_name
        assert name_to_set in name

    def test_set_job_names_using_own_default(self):
        """Test set_job_names utils function with using own default name."""
        def_name = "def_job_name"
        name_to_set = None
        orig_name, name = set_job_names(name_to_set, default_name=def_name)
        assert def_name == orig_name
        assert "job" in name

    def test_set_job_names_using_default(self):
        """Test set_job_names utils function with using default name."""
        name_to_set = None
        orig_name, name = set_job_names(name_to_set)
        assert "unknown_job" == orig_name
        assert "job" in name

    def test_create_actinia_pc_item(self):
        """Test set_job_names utils function with using default name."""
        module = "g.region"
        id = "pc_item_ide"
        inputs = {
            "raster": "elevation@PERMANENT",
            "res": "5000",
        }
        pc_item = create_actinia_pc_item(
            id=id,
            module="g.region",
            inputs=inputs,
            flags="g",
        )
        assert "module" in pc_item
        assert "id" in pc_item
        assert "inputs" in pc_item
        assert pc_item["module"] == module
        assert pc_item["id"] == id
        assert isinstance(pc_item["inputs"], list)
        for inp in pc_item["inputs"]:
            param = inp["param"]
            value = inp["value"]
            assert param in inputs
            assert inputs[param] == value
