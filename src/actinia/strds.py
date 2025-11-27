#!/usr/bin/env python

"""The strds module provides a class for SpaceTimeRasterDataset handling.

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
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from actinia.resources.logger import log
from actinia.utils import request_and_check

if TYPE_CHECKING:
    from actinia import Actinia


class SpaceTimeRasterDataset:
    """Class for SpaceTimeRasterDataset (STRDS) operations."""

    def __init__(
        self,
        name: str,
        location_name: str,
        mapset_name: str,
        actinia: Actinia,
        auth: tuple,
    ) -> None:
        """Initialize the SpaceTimeRasterDataset (STRDS) object."""
        self.name = name
        self.__location_name = location_name
        self.__mapset_name = mapset_name
        self.__actinia = actinia
        self.__auth = auth
        self.raster_layers = None
        self.info = None

    def get_info(self, *, force: Optional(bool) = False) -> dict:
        """Return the information of the SpaceTimeRasterDataset (STRDS).

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
        """Return a list of Raster Layers from a SpaceTimeRasterDataset.

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
        if self.raster_layers is None or force is True:
            url = (
                f"{self.__actinia.url}/locations/{self.__location_name}/"
                f"mapsets/{self.__mapset_name}/strds/{self.name}/raster_layers"
            )
            if where:
                url += f"?where={where}"
            # Empty STRDS returns status code 400
            resp = request_and_check("GET", url, auth=self.__auth, status_code=(200,400,))
            if "Dataset is empty" in resp["stderr"]:
                log.info("No raster layer found in STRDS <%s>.", self.name)
                self.raster_layers = {}
            elif resp["http_code"] == 400:
                raise RuntimeError("Request failed with the following response:\n%s", resp)
            else:
                self.raster_layers = resp["process_results"]

        return self.raster_layers

    def register_raster_layer(
        self,
        name: str,
        start_time: str | datetime,
        end_time: str | datetime = "",
    ) -> None:
        """Register a Raster Layer in a SpaceTimeRasterDataset (STRDS).

        Parameters
        ----------
        name: string
            Name of the raster layer to register in STRDS
        start_time: string
            Start time of the raster layer to register in STRDS
        end_time: string | datetime
            End time of the raster layer to register in STRDS
            Can be empty (default).

        """
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
        """Unregister Raster Layers from a SpaceTimeRasterDataset (STRDS).

        Parameters
        ----------
        raster_layers: list of strings
            List with names of the raster layers to unregister
            from STRDS

        """
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

    def sample_strds(
        self,
        points: list[list[str]] | dict | Path | str,
        *,
        async_request: bool = False,
    ) -> dict:
        """Sample SpaceTimeRasterDataset at point locations.

        Parameters
        ----------
        points: list[tuple] | dict | Path | str
            Point locations to sample
        async_request: bool
            If True, the request is sent asynchronously

        Returns
        -------
        strds_values: dict
            Values of the SpaceTimeRasterDataset
            at point locations

        Raises
        ------
        OSError
            OSError if input file does not exist.

        """
        postkwargs = {
            "headers": self.__actinia.headers,
            "auth": self.__auth,
            "timeout": self.__actinia.timeout,
        }
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.__mapset_name}/strds/{self.name}"
        )
        if isinstance(points, str):
            points = Path(points)
        if isinstance(points, Path):
            if not points.exists():
                msg = f"File <{points}> does not exist"
                raise OSError(msg)
            url += f"sampling_{'a' if async_request else ''}sync_geojson"
            postkwargs["data"] = points.read_text(encoding="UTF8")
        else:
            if isinstance(points, list):
                postkwargs["data"] = json.dumps({"points": points})
            else:
                postkwargs["data"] = json.dumps(points)
            url += f"sampling_{'a' if async_request else ''}sync"
        return request_and_check("POST", url, **postkwargs)

    def compute_strds_statistics(
        self,
        polygon: dict | Path | str,
        timestamp: Optional(datetime) = None,
        *,
        async_request: bool = False,
    ) -> dict:
        """Compute SpaceTimeRasterDataset statistics within polygon.

        Parameters
        ----------
        polygon: list[tuple] | dict | Path | str
            Polygon to compute statistics for either as list of tuples
            with valid coordinates, GeoJSON dict, or path to GeoJSON file
        timestamp: datetime | None
            Timestamp to compute statistics for
        async_request: bool
            If True, the request is sent asynchronously

        Returns
        -------
        strds_statistics: dict
            Statistics of the SpaceTimeRasterDataset

        Raises
        ------
        OSError
            OSError if input file is not found.

        """
        postkwargs = {
            "headers": self.__actinia.headers,
            "auth": self.__auth,
            "timeout": self.__actinia.timeout,
        }
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.__mapset_name}/strds/{self.name}"
            f"timestamp/{timestamp.strftime('%Y-%m-%dT%H:%M:%S')}"
        )
        if isinstance(polygon, str):
            polygon = Path(polygon)
        if isinstance(polygon, Path):
            if not polygon.exists():
                msg = f"File <{polygon}> does not exist"
                raise OSError(msg)
            url += f"sampling_{'a' if async_request else ''}sync_geojson"
            postkwargs["data"] = polygon.read_text(encoding="UTF8")
        else:
            postkwargs["data"] = json.dumps(polygon)
            url += f"sampling_{'a' if async_request else ''}sync"
        return request_and_check("POST", url, **postkwargs)

    def render(self, render_dict: dict) -> dict:
        """Render Raster layers in a SpaceTimeRasterDataset (STRDS).

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
