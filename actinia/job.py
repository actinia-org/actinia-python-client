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
import logging
import requests
import sys


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
        self.accept_datetime = actinia_json_dict.get("accept_datetime")
        self.accept_timestamp = actinia_json_dict.get("accept_timestamp")
        self.api_info = actinia_json_dict.get("api_info")
        self.datetime = actinia_json_dict.get("datetime")
        self.http_code = actinia_json_dict.get("http_code")
        self.message = actinia_json_dict.get("message")
        self.process_chain_list = actinia_json_dict.get("process_chain_list")
        self.process_results = actinia_json_dict.get("process_results")
        self.resource_id = actinia_json_dict.get("resource_id")
        self.status = actinia_json_dict.get("status")
        self.time_delta = actinia_json_dict.get("time_delta")
        self.timestamp = actinia_json_dict.get("timestamp")
        self.urls = actinia_json_dict.get("urls")
        self.user_id = actinia_json_dict.get("user_id")

    def __update(
        self,
        actinia_json_dict,
    ):
        self.datetime = actinia_json_dict.get("datetime")
        self.http_code = actinia_json_dict.get("http_code")
        self.message = actinia_json_dict.get("message")
        self.process_results = actinia_json_dict.get("process_results")
        self.status = actinia_json_dict.get("status")
        self.time_delta = actinia_json_dict.get("time_delta")
        self.timestamp = actinia_json_dict.get("timestamp")
        self.urls = actinia_json_dict.get("urls")

    def poll(self):
        """
        Update job by polling.
        """
        if self.status not in ["accepted", "running"]:
            logging.warning("The job is not running and can not be updated.")

        kwargs = dict()
        kwargs["headers"] = self.__actinia.headers
        kwargs["auth"] = self.__auth
        url = self.urls["status"]
        try:
            actiniaResp = requests.get(url, **kwargs)
        except requests.exceptions.ConnectionError as e:
            raise e
        resp = json.loads(actiniaResp.text)

        if "process_results" not in resp:
            resp["process_results"] = {}
        self.__update(
            resp,
        )
        print(f"Status of {self.name} job is {self.status}.", file=sys.stdout)

    def poll_until_finished(self):
        """
        Polling job until finished or error.
        """
        status_accepted_running = True
        while status_accepted_running:
            self.poll()
            if self.status not in ["accepted", "running"]:
                status_accepted_running = False
                msg = f"Status of {self.name} job is {self.status}: " \
                    f"{self.message}"
                print(msg, file=sys.stderr)

    # def terminate(self):
    #     """
    #     Terminate job.
    #     """
    #
    # TODO
