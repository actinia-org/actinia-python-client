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
        accept_datetime,
        accept_timestamp,
        api_info,
        datetime,
        http_code,
        message,
        process_chain_list,
        process_results,
        resource_id,
        status,
        time_delta,
        timestamp,
        urls,
        user_id,
        queue,
        **args
    ):
        self.name = name
        self.__actinia = actinia
        self.__auth = auth
        self.accept_datetime = accept_datetime
        self.accept_timestamp = accept_timestamp
        self.api_info = api_info
        self.datetime = datetime
        self.http_code = http_code
        self.message = message
        self.process_chain_list = process_chain_list
        self.process_results = process_results
        self.resource_id = resource_id
        self.status = status
        self.time_delta = time_delta
        self.timestamp = timestamp
        self.urls = urls
        self.user_id = user_id
        self.queue = queue

    def __update(
        self,
        datetime,
        http_code,
        message,
        process_results,
        status,
        time_delta,
        timestamp,
        urls,
    ):
        self.datetime = datetime
        self.http_code = http_code
        self.message = message
        self.process_results = process_results
        self.status = status
        self.time_delta = time_delta
        self.timestamp = timestamp
        self.urls = urls

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
            resp["datetime"],
            resp["http_code"],
            resp["message"],
            resp["process_results"],
            resp["status"],
            resp["time_delta"],
            resp["timestamp"],
            resp["urls"],
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
