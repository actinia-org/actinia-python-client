#!/usr/bin/env python

"""The strds module provides a class for SpaceTimeRasterDataSet (STRDS) operations.

actinia-python-client is a python client for actinia - an open source REST
API for scalable, distributed, high performance processing of geographical
data that uses GRASS GIS for computational tasks.

Copyright (c) 2024 mundialis GmbH & Co. KG

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from __future__ import annotations

__license__ = "GPLv3"
__author__ = "Anika Weinmann, Stefan Blumentrath"
__copyright__ = "Copyright 2022-2024, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import json
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from actinia.utils import request_and_check

if TYPE_CHECKING:
    from actinia import Actinia


class SpaceTimeRasterDataSet:
    """Class for SpaceTimeRasterDataSet (STRDS) operations."""

    def __init__(
        self,
        name: str,
        location_name: str,
        mapset_name: str,
        actinia: Actinia,
        auth: tuple,
    ) -> None:
        """Initialize the SpaceTimeRasterDataSet (STRDS) object."""
        self.name = name
        self.__location_name = location_name
        self.__mapset_name = mapset_name
        self.__actinia = actinia
        self.__auth = auth
        self.raster_layers = None
        self.info = None

    def get_info(self, *, force: Optional(bool) = False) -> dict:
        """Return the information of the SpaceTimeRasterDataSet (STRDS).

        Parameters
        ----------
        force: bool
            Force uptating STRDS info

        Returns
        -------
        info: dict
            dict with information about the SpaceTimeRasterDataset

        """
        if self.info is None or force is True:
            url = (
                f"{self.__actinia.url}/locations/{self.__location_name}/"
                f"mapsets/{self.__mapset_name}/strds/{self.name}"
            )
            resp = request_and_check("GET", url, auth=self.__auth)
            strds_info = resp["process_results"]
            self.info = strds_info
        return self.info

    def get_strds_raster_layers(
        self,
        where: Optional(str) = None,
        *,
        force: Optional(bool) = False,
    ) -> dict:
        """Return a list of Raster Layers from a SpaceTimeRasterDataSet.

        Parameters
        ----------
        where: str
            String with WHERE-clause for a STRDS-where-query without
            WHERE keyword
        force: bool
            Force uptating STRDS info

        Returns
        -------
        info: dict
            dict with information about the SpaceTimeRasterDataset

        """
        if self.info is None or force is True:
            url = (
                f"{self.__actinia.url}/locations/{self.__location_name}/"
                f"mapsets/{self.__mapset_name}/strds/{self.name}"
            )
            if where:
                url += f"?where={where}"
            resp = request_and_check("GET", url, auth=self.__auth)
            raster_layers = resp["process_results"]
            self.raster_layers = raster_layers
        return self.info

    def register_raster_layer(
        self,
        name: str,
        start_time: str | datetime,
        end_time: str | datetime,
    ) -> None:
        """Register a Raster Layer in a SpaceTimeRasterDataSet (STRDS)."""
        if isinstance(start_time, datetime):
            start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(end_time, datetime):
            end_time = end_time.strftime("%Y-%m-%d %H:%M:%S")
        putkwargs = {
            "headers": self.__actinia.headers,
            "auth": self.__auth,
            "timeout": self.__actinia.timeout,
            "data": json.dumps(
                {"name": name, "start_time": start_time, "end_time": end_time},
            ),
        }
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.__mapset_name}/strds/{self.name}/raster_layers"
        )
        request_and_check("PUT", url, **putkwargs)

    def unregister_raster_layers(self, raster_layers: list[str]) -> None:
        """Unregister Raster Layers from a SpaceTimeRasterDataSet (STRDS)."""
        delkwargs = {
            "headers": self.__actinia.headers,
            "auth": self.__auth,
            "timeout": self.__actinia.timeout,
            "data": json.dumps(raster_layers),
        }
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.__mapset_name}/strds/{self.name}/raster_layers"
        )
        request_and_check("DEL", url, **delkwargs)

    def render(self, render_dict: dict) -> dict:
        """Render Raster layers in a SpaceTimeRasterDataSet (STRDS).

        Returns
        -------
        render: dict
            dict with render response.

        Raises
        ------
        ValueError:
            ValueError if dict does not containt required keys.

        """
        if set(render_dict.keys()) != {
            "n",
            "s",
            "e",
            "w",
            "width",
            "height",
            "start_time",
            "end_time",
        }:
            msg = (
                "render_dict must contain the keys"
                " 'n', 's', 'e', 'w', 'width', 'height',"
                " 'start_time', 'end_time'"
            )
            raise ValueError(msg)
        getkwargs = {
            "headers": self.__actinia.headers,
            "auth": self.__auth,
            "timeout": self.__actinia.timeout,
            "data": json.dumps(render_dict),
        }
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.__mapset_name}/strds/{self.name}/render"
        )
        return request_and_check("GET", url, **getkwargs)
