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
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2023, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

from actinia import Actinia
from actinia.job import Job

from .actinia_config import (
    ACTINIA_BASEURL,
    ACTINIA_VERSION,
    ACTINIA_AUTH,
    LOCATION_NAME,
)

PC = {
    "list": [
        {
            "id": "r_mapcalc",
            "module": "r.mapcalc",
            "inputs": [{"param": "expression", "value": "elevation=42"}],
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
            ],
        }
    ],
    "version": "1",
}


class TestActiniaLocation(object):
    @classmethod
    def setup_class(cls):
        cls.testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(cls.testactinia, Actinia)
        cls.testactinia.set_authentication(ACTINIA_AUTH[0], ACTINIA_AUTH[1])
        cls.testactinia.get_locations()

    def test_async_process_chain_validation(self):
        """Test async process chain validation."""
        val_job = self.testactinia.locations[
            LOCATION_NAME
        ].validate_process_chain_async(PC)
        assert isinstance(val_job, Job), "No job returned!"
        # poll job
        val_job.poll_until_finished()
        assert val_job.status == "finished", "Job status not 'finished'!"
        assert (
            val_job.message == "Validation successful"
        ), "Validation stdout not correct"

    def test_async_process_chain_validation_error(self):
        """Test async process chain validation error."""
        val_job = self.testactinia.locations[
            LOCATION_NAME
        ].validate_process_chain_async(PC_error)
        assert isinstance(val_job, Job), "No job returned!"
        # poll job
        val_job.poll_until_finished()
        assert val_job.status == "error", "Job status not 'error'!"
        assert (
            "AsyncProcessError" in val_job.message
        ), "Validation job message not correct!"
