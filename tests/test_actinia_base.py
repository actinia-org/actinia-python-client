#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# acintia-python-client is a python client for actinia - an open source REST
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
import pytest
from unittest.mock import Mock, patch

from actinia import Actinia

from .mock.actinia_mock import ACTINIA_BASEURL, version_resp_text

__author__ = "Anika Weinmann"
__copyright__ = "mundialis"
__license__ = "TODO"


class TestActiniaAuth(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch("actinia.actinia.requests.get")
        cls.mock_get = cls.mock_get_patcher.start()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()

    def test_actinia_base(self):
        """Base test of actinia with a version check."""
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(version_resp_text)

        testactinia = Actinia(ACTINIA_BASEURL)
        assert isinstance(testactinia, Actinia)

        version = testactinia.get_version()
        assert "grass_version" in version
        assert "plugins" in version
        assert "version" in version

    def test_auth(self):
        """Test the authentication setting."""
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(version_resp_text)

        testactinia = Actinia(ACTINIA_BASEURL)
        assert isinstance(testactinia, Actinia)

        try:
            testactinia.set_authentication("user", "pw")
        except Exception as e:
            raise pytest.fail(f"Authentication raises: {e}")

    def test_wrong_auth(self):
        """Test the behavior when a wrong authentication is set."""
        # Configure the mock
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(version_resp_text)

        testactinia = Actinia(ACTINIA_BASEURL)
        assert isinstance(testactinia, Actinia)

        # check wrong auth behavior
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 401

        with pytest.raises(Exception) as e:
            testactinia.set_authentication("user", "pw")

        assert e.type == Exception
        assert (
            str(e.value) == "Wrong user or password. Please check your inputs."
        )
