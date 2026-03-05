#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# SPDX-FileCopyrightText: (c) 2022 mundialis GmbH & Co. KG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#######

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import json
import requests
from datetime import datetime


def request_and_check(method, url, status_code=(200,), retries=0, **kwargs):
    """Send a request with the given method to a URL and check the status code.

    Parameters:
        method (string): Request method (GET, POST, PUT, DELETE, ...)
        url (string): URL as string
        status_code (tuple): Tuple of acceptable status codes to check
                             if it is set; default is 200
        retries (int): Maximal number of retries in case of read timeouts
            default is 0.
        **kwargs:
            auth (tuple): Tuple of user and password
            timeout (tuple): Tuple of connection timeout and read timeout
            headers (dict): Request headers
            data (str): Request body to send (if needed)

    Returns:
        (dict): returns text of the response as dictionary

    Throws an error if the request does not have the right status_code or
    the response content cannot be paresd as JSON.
    """
    attempt = 0
    while attempt <= retries:
        attempt += 1
        resp = requests.request(method, url, **kwargs)
        try:
            if resp.status_code not in status_code:
                resp.raise_for_status()
        except requests.exceptions.ReadTimeout as e:
            if attempt >= retries:
                raise e
            continue
        except requests.exceptions.RequestException as e:
            if resp.status_code == 401:
                raise Exception(
                    "Wrong user or password. Please check your inputs."
                ) from e
            raise requests.exceptions.RequestException(
                f"Error {resp.status_code}: {resp.text}", e
            ) from None
    try:
        return json.loads(resp.text)
    except json.JSONDecodeError:
        raise RuntimeError(
            "Invalid value returned. Cannot parse JSON from response:",
            resp.text,
        ) from None


def set_job_names(name, default_name="unknown_job"):
    """Function to set the date/time to the job name"""
    now = datetime.now()
    if name is None:
        orig_name = default_name
        name = f"job_{now.strftime('%Y%d%m_%H%M%S')}"
    else:
        orig_name = name
        name += f"_{now.strftime('%Y%d%m_%H%M%S')}"
    return orig_name, name


def create_actinia_pc_item(
    id,
    module,
    inputs=None,
    outputs=None,
    flags=None,
    stdin=None,
    stdout=None,
    overwrite=False,
    superquiet=False,
    verbose=False,
    interface_description=False,
):
    """
    Creates a list item for an actinia process chain

    Parameters
    ----------
    id: str
        unique id for this item
    module: str
        some valid GRASS or actinia module
    inputs: list or dict
        list of input parameters with values in the form
        [{"param": key1, "value": value1}, {"param": key2, "value": value2},
        ...]
        shorter alternative as dict
        {"key1": value1, "key2": value2, ...}
    outputs: list or dict
        list of output parameters with values in the form
        [{"param": key1, "value": value1}, {"param": key2, "value": value2},
        ...]
        shorter alternative as dict
        {"key1": value1, "key2": value2, ...}
    flags: str
        optional flags for the module
    stdin: dict
        options to read stdin
    stdout: dict
        options to write to stdout
        must be of the form
        {"id": value1, "format": value2, "delimiter": value3}
    overwrite: bool
        optional, set to True to allow overwriting existing data
    superquiet: bool
        optional, set to True to suppress all messages but errors
    verbose: bool
        optional, set to True to allow verbose messages
    interface_description: bool
        optional, set to True to create an interface_description
    """
    pc_item = {"id": str(id), "module": module}
    if inputs:
        if isinstance(inputs, list):
            pc_item["inputs"] = inputs
        elif isinstance(inputs, dict):
            tmplist = []
            for k, v in inputs.items():
                tmplist.append({"param": k, "value": v})
            pc_item["inputs"] = tmplist
    if outputs:
        if isinstance(outputs, list):
            pc_item["outputs"] = outputs
        elif isinstance(outputs, dict):
            tmplist = []
            for k, v in outputs.items():
                tmplist.append({"param": k, "value": v})
            pc_item["outputs"] = tmplist
    if flags:
        pc_item["flags"] = flags
    if stdin:
        pc_item["stdin"] = stdin
    if stdout:
        pc_item["stdout"] = stdout
    if overwrite is True:
        pc_item["overwrite"] = True
    if superquiet is True:
        pc_item["superquiet"] = True
    if verbose is True:
        pc_item["verbose"] = True
    if interface_description is True:
        pc_item["interface_description"] = True

    return pc_item
