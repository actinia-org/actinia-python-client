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

from copy import deepcopy

from .actinia_mock import ACTINIA_BASEURL, ACTINIA_VERSION


process_chain_validation_sync = {
    'accept_datetime': '2022-05-25 12:02:16.251628',
    'accept_timestamp': 1653480136.2516265,
    'api_info':
        {
            'endpoint': 'syncprocessvalidationresource',
            'method': 'POST',
            'path': f'/api/{ACTINIA_VERSION}/locations/nc_spm_08/'
                    'process_chain_validation_sync',
            'request_url': f'{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations'
                           '/nc_spm_08/process_chain_validation_sync'
        },
    'datetime': '2022-05-25 12:02:16.711651',
    'http_code': 200,
    'message': 'Validation successful',
    'process_chain_list':
    [{
        'list':
        [{
            'id': 'r_mapcalc',
            'inputs':
                [{'param': 'expression', 'value': 'elevation=42'}],
            'module': 'r.mapcalc'
        }],
        'version': '1'
    }],
    'process_log': [],
    'process_results': ["grass r.mapcalc ['expression=elevation=42']"],
    'progress':
    {'num_of_steps': 1, 'step': 0},
    'resource_id': 'resource_id-63f35ae0-797c-436c-a9ac-28a457b011a3',
    'status': 'finished',
    'time_delta': 0.4600515365600586,
    'timestamp': 1653480136.7116203,
    'urls': {
        'resources': [],
        'status':
            f'{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser'
            '/resource_id-63f35ae0-797c-436c-a9ac-28a457b011a3'
            },
    'user_id': 'testuser'
}


process_chain_validation_sync_err = {
    'accept_datetime': '2022-05-25 13:08:16.553306',
    'accept_timestamp': 1653484096.5533047,
    'api_info': {
        'endpoint': 'syncprocessvalidationresource',
        'method': 'POST',
        'path': f'/api/{ACTINIA_VERSION}/locations/nc_spm_08/'
                'process_chain_validation_sync',
        'request_url': f'{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/'
                       'nc_spm_08/process_chain_validation_sync'
    },
    'datetime': '2022-05-25 13:08:17.024130',
    'exception': {
        'message': 'AsyncProcessError:  <value> is missing in input '
                   'description of process id: r_mapcalc',
        'traceback': [
            '  File "/usr/lib/python3.8/site-packages/actinia_core/'
            'rest/ephemeral_processing.py", line 1767, in run\n    '
            'self._execute()\n', '  File "/usr/lib/python3.8/site-packages/'
            'actinia_core/rest/process_validation.py", line 148, in _execute\n'
            '    process_chain = self._create_temporary_grass_environment_'
            'and_process_list()\n', '  File "/usr/lib/python3.8/site-packages/'
            'actinia_core/rest/ephemeral_processing.py", line 1647, in '
            '_create_temporary_grass_environment_and_process_list\n    '
            'process_list = self._validate_process_chain(\n', '  File "/usr/'
            'lib/python3.8/site-packages/actinia_core/rest/ephemeral_'
            'processing.py", line 666, in _validate_process_chain\n    '
            'process_list = self.proc_chain_converter.process_chain_to_process'
            '_list(\n', '  File "/usr/lib/python3.8/site-packages/actinia_core'
            '/core/common/process_chain.py", line 127, in process_chain_to_'
            'process_list\n    return self._process_chain_to_process_list('
            'process_chain)\n', '  File "/usr/lib/python3.8/site-packages/'
            'actinia_core/core/common/process_chain.py", line 176, in _process'
            '_chain_to_process_list\n    module = self._create_module_process'
            '(process_descr)\n', '  File "/usr/lib/python3.8/site-packages/'
            'actinia_core/core/common/process_chain.py", line 424, in _create'
            '_module_process\n    self._add_grass_module_input_parameter_to_'
            'list(\n', '  File "/usr/lib/python3.8/site-packages/actinia_core/'
            'core/common/process_chain.py", line 875, in _add_grass_module_'
            'input_parameter_to_list\n    raise AsyncProcessError(\n'],
        'type': "<class 'actinia_core.core.common.exceptions."
                "AsyncProcessError'>"
    },
    'http_code': 400,
    'message': 'AsyncProcessError:  <value> is missing in input description '
               'of process id: r_mapcalc',
    'process_chain_list': [],
    'process_log': [],
    'progress': {
        'num_of_steps': 0,
        'step': 0
    },
    'resource_id': 'resource_id-1afc7cf3-e01a-4d93-82ce-288aa01bbaed',
    'status': 'error',
    'time_delta': 0.47088122367858887,
    'timestamp': 1653484097.0240579,
    'urls': {
        'resources': [],
        'status': f'{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser'
                  '/resource_id-1afc7cf3-e01a-4d93-82ce-288aa01bbaed'
    },
    'user_id': 'testuser'
}

process_chain_validation_async = {
    'accept_datetime': '2022-05-25 14:06:38.933988',
    'accept_timestamp': 1653487598.9339852,
    'api_info': {
        'endpoint': 'asyncprocessvalidationresource',
        'method': 'POST',
        'path': f'/api/{ACTINIA_VERSION}/locations/nc_spm_08/'
                'process_chain_validation_async',
        'request_url': f'{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/'
                       'nc_spm_08/process_chain_validation_async'
    },
    'datetime': '2022-05-25 14:06:38.935917',
    'http_code': 200,
    'message': 'Resource accepted',
    'process_chain_list': [],
    'process_results': {},
    'resource_id': 'resource_id-031d34cf-f601-448b-81e9-1c50ff9532e2',
    'status': 'accepted',
    'time_delta': 0.0019378662109375,
    'timestamp': 1653487598.9359155,
    'urls': {
        'resources': [],
        'status': f'{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/resources/testuser'
                  '/resource_id-031d34cf-f601-448b-81e9-1c50ff9532e2'
    },
    'user_id': 'testuser'
}

process_chain_validation_async_poll = deepcopy(process_chain_validation_sync)
process_chain_validation_async_poll["api_info"]["endpoint"] = \
    "asyncprocessvalidationresource"
process_chain_validation_async_poll["api_info"]["path"] = \
    f"/api/{ACTINIA_VERSION}/locations/nc_spm_08/process_chain_" \
    "validation_async"
process_chain_validation_async_poll["api_info"]["request_url"] = \
    f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/nc_spm_08/process_" \
    "chain_validation_async"
process_chain_validation_async_poll["resource_id"] = \
    process_chain_validation_async["resource_id"]
process_chain_validation_async_poll["urls"]["status"] = \
    process_chain_validation_async["urls"]["status"]

process_chain_validation_async_err_poll = deepcopy(
    process_chain_validation_sync_err)
process_chain_validation_async_err_poll["api_info"]["endpoint"] = \
    "asyncprocessvalidationresource"
process_chain_validation_async_err_poll["api_info"]["path"] = \
    f"/api/{ACTINIA_VERSION}/locations/nc_spm_08/process_chain_" \
    "validation_async"
process_chain_validation_async_err_poll["api_info"]["request_url"] = \
    f"{ACTINIA_BASEURL}/api/{ACTINIA_VERSION}/locations/nc_spm_08/" \
    "process_chain_validation_async"
process_chain_validation_async_err_poll["resource_id"] = \
    process_chain_validation_async["resource_id"]
