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

from time import sleep

from actinia.resources.logger import log
from actinia.utils import request_and_check


class Job:
    def __init__(
        self,
        name,
        actinia,
        auth,
        actinia_json_dict,
    ):
        self.name = name
        self.__actinia = actinia
        self.__auth = auth
        for key in actinia_json_dict:
            setattr(self, key, actinia_json_dict[key])

    def __update(
        self,
        actinia_json_dict,
    ):
        for key in actinia_json_dict:
            setattr(self, key, actinia_json_dict[key])

    def poll(self, quiet=False):
        """
        Update job by polling.
        """
        if self.status not in ["accepted", "running"]:
            log.warning("The job is not running and can not be updated.")

        kwargs = {
            "headers": self.__actinia.headers,
            "auth": self.__auth,
            "timeout": self.__actinia.timeout,
        }
        url = self.urls["status"]
        resp = request_and_check("GET", url, status_code=(200, 400), **kwargs)

        if "process_results" not in resp:
            resp["process_results"] = {}
        self.__update(
            resp,
        )
        if not quiet:
            log.info(f"Status of {self.name} job is {self.status}.")

    def poll_until_finished(self, waiting_time=5, quiet=False):
        """
        Polling job until finished or error.

        Args:
            waiting_time: Time to wait in seconds for next poll
            quiet: Bool if the method should log each process status or only
                   changed
        """
        status_accepted_running = True
        status = None
        while status_accepted_running:
            self.poll(quiet=True)
            if self.status not in ["accepted", "running"]:
                status_accepted_running = False
                msg = f"Status of {self.name} job is {self.status}: " f"{self.message}"
                if self.status in ["terminated", "error"]:
                    log.error(msg)
                    return 1
                elif self.status in ["finished"]:
                    log.info(msg)
                    return 0
            sleep(waiting_time)
            if self.status != status and not quiet:
                status = self.status
                msg = f"Status of {self.name} job is {self.status}: " f"{self.message}"
                log.info(msg)

    def terminate(self):
        """Terminate the current job"""
        kwargs = {"auth": self._Job__auth, "timeout": self.__actinia.timeout}
        url = f"{self._Job__actinia.url}/resources/{self.user_id}/{self.resource_id}"
        request_and_check("DELETE", url, **kwargs)
        log.info("Termination request for job {self.resource_id} committed.")
