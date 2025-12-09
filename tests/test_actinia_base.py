#!/usr/bin/env python
# -*- coding: utf-8 -*-
#######
# actinia-python-client is a python client for actinia - an open source REST
# API for scalable, distributed, high performance processing of geographical
# data that uses GRASS GIS for computational tasks.
#
# SPDX-FileCopyrightText: (c) 2022-2023 mundialis GmbH & Co. KG
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
#######

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2022-2023, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import pytest

from actinia import Actinia

from .actinia_config import ACTINIA_BASEURL, ACTINIA_VERSION, ACTINIA_AUTH

__license__ = "GPL-3.0-or-later"
__author__ = "Anika Weinmann"
__copyright__ = "Copyright 2023, mundialis GmbH & Co. KG"


class TestActiniaAuth(object):
    def test_actinia_base(self):
        """Base test of actinia with a version check."""

        testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(testactinia, Actinia)

        version = testactinia.get_version()
        assert "grass_version" in version
        assert "plugins" in version
        assert "version" in version

    def test_auth(self):
        """Test the authentication setting."""

        testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(testactinia, Actinia)

        try:
            testactinia.set_authentication(ACTINIA_AUTH[0], ACTINIA_AUTH[1])
        except Exception as e:
            raise pytest.fail(f"Authentication raises: {e}")

    def test_wrong_auth(self):
        """Test the behavior when a wrong authentication is set."""

        testactinia = Actinia(ACTINIA_BASEURL, ACTINIA_VERSION)
        assert isinstance(testactinia, Actinia)

        with pytest.raises(Exception) as e:
            testactinia.set_authentication("user", "pw")

        assert e.type == Exception
        assert (
            str(e.value) == "Wrong user or password. Please check your inputs."
        )
