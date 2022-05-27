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
from io import StringIO

from actinia import Actinia
from actinia.job import Job

from .mock.actinia_mock import (
    ACTINIA_BASEURL,
    version_resp_text,
)
from .mock.actinia_location_management_mock import get_locations_resp
from .mock.actinia_process_chain_validation_mock import (
    process_chain_validation_sync,
    process_chain_validation_sync_err,
    process_chain_validation_async,
    process_chain_validation_async_poll,
    process_chain_validation_async_err_poll,
)

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
PC_error = {
    "list": [
      {
          "id": "r_mapcalc",
          "module": "r.mapcalc",
          "inputs": [
              {
                  "param": "expression",
              }
          ]
      }
    ],
    "version": "1"
}


class TestActiniaLocation(object):
    @classmethod
    def setup_class(cls):
        cls.mock_post_patcher = patch("actinia.actinia.requests.post")
        cls.mock_get_patcher = patch("actinia.actinia.requests.get")
        cls.mock_post = cls.mock_post_patcher.start()
        cls.mock_get = cls.mock_get_patcher.start()
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
        cls.mock_post_patcher.stop()

    @patch('sys.stdout', new_callable=StringIO)
    def test_sync_process_chain_validation(self, stdout):
        """Test sync process chain validation."""
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.text = json.dumps(
            process_chain_validation_sync)
        self.testactinia.locations[
            LOCATION_NAME].validate_process_chain_sync(PC)
        assert stdout.getvalue() == "Validation successful\n", \
            "Validation stdout not correct"

    @patch('sys.stderr', new_callable=StringIO)
    def test_sync_process_chain_validation_error(self, stderr):
        """Test sync process chain validation error."""
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 400
        self.mock_post.return_value.text = json.dumps(
            process_chain_validation_sync_err)
        self.testactinia.locations[
            LOCATION_NAME].validate_process_chain_sync(PC_error)
        assert "Validation error:" in stderr.getvalue(), \
            "Validation stderr not correct by validation error"

    def test_async_process_chain_validation(self):
        """Test async process chain validation."""
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.text = json.dumps(
            process_chain_validation_async)
        val_job = self.testactinia.locations[
            LOCATION_NAME].validate_process_chain_async(PC)
        assert isinstance(val_job, Job), "No job returned!"
        # mock polling and poll job
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(
            process_chain_validation_async_poll)
        val_job.poll_until_finished()
        assert val_job.status == "finished", "Job status not 'finished'!"
        assert val_job.message == "Validation successful", \
            "Validation stdout not correct"

    def test_async_process_chain_validation_error(self):
        """Test async process chain validation error."""
        self.mock_post.return_value = Mock()
        self.mock_post.return_value.status_code = 200
        self.mock_post.return_value.text = json.dumps(
            process_chain_validation_async)
        val_job = self.testactinia.locations[
            LOCATION_NAME].validate_process_chain_async(PC)
        assert isinstance(val_job, Job), "No job returned!"
        # mock polling and poll job
        self.mock_get.return_value = Mock()
        self.mock_get.return_value.status_code = 200
        self.mock_get.return_value.text = json.dumps(
            process_chain_validation_async_err_poll)
        val_job.poll_until_finished()
        assert val_job.status == "error", "Job status not 'error'!"
        assert "AsyncProcessError" in val_job.message, \
            "Validation job message not correct!"
