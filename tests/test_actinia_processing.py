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
from unittest.mock import Mock, patch

from actinia import Actinia

from .mock.actinia_mock import (
    ACTINIA_BASEURL,
    version_resp_text,
    start_job_resp,
    job_poll_resp,
)
from .mock.actinia_location_management_mock import get_locations_resp

__license__ = "GPLv3"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"

LOCATION_NAME = "nc_spm_08"
PC = {
    "list": [
        {
            "id": "r_mapcalc",
            "module": "r.mapcalc",
            "inputs": [{"param": "expression", "value": "baum=5"}],
        }
    ],
    "version": "1",
}


class TestActiniaLocation(object):
    @classmethod
    def setup_class(cls):
        cls.mock_get_patcher = patch("actinia.actinia.requests.get")
        cls.mock_post_patcher = patch("actinia.actinia.requests.post")
        cls.mock_get = cls.mock_get_patcher.start()
        cls.mock_post = cls.mock_post_patcher.start()

        cls.mock_get.return_value = Mock()
        cls.mock_get.return_value.status_code = 200
        cls.mock_get.return_value.text = json.dumps(version_resp_text)
        cls.testactinia = Actinia(ACTINIA_BASEURL)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication("user", "pw")
        # get locations
        cls.mock_get.return_value = Mock()
        cls.mock_get.return_value.status_code = 200
        cls.mock_get.return_value.text = json.dumps(get_locations_resp)
        cls.testactinia.get_locations()

    @classmethod
    def teardown_class(cls):
        cls.mock_get_patcher.stop()
        cls.mock_post_patcher.stop()

    def test_location_create_job_pcdict(self):
        """Test location get_mapsets method with a simple PC dict."""
        assert len(self.testactinia.jobs) == 0

        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.text = json.dumps(start_job_resp)
        self.mock_get.return_value.text = json.dumps(job_poll_resp)

        testjob = self.testactinia.locations[
            LOCATION_NAME
        ].create_processing_export_job(PC)

        assert testjob.name == "unknown_job"
        assert testjob.status == "accepted"
        assert len(self.testactinia.jobs) == 1

        # poll job
        testjob.poll_until_finished()
        assert testjob.status == "finished"
