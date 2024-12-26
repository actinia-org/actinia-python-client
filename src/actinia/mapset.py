#!/usr/bin/env python

"""The mapset module provides a Mapset class to interact with mapsets.

actinia-python-client is a python client for actinia - an open source REST
API for scalable, distributed, high performance processing of geographical
data that uses GRASS GIS for computational tasks.

Copyright (c) 2022 mundialis GmbH & Co. KG

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
__author__ = "Anika Weinmann, Corey White and Stefan Blumentrath"
__copyright__ = "Copyright 2022, mundialis GmbH & Co. KG"
__maintainer__ = "Anika Weinmann"

import json
from datetime import datetime
from enum import Enum, unique
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from actinia import Actinia
from actinia.job import Job
from actinia.raster import Raster
from actinia.region import Region
from actinia.resources.logger import log
from actinia.strds import SpaceTimeRasterDataset
from actinia.utils import request_and_check, set_job_names
from actinia.vector import Vector

if TYPE_CHECKING:
    from actinia import Actinia


@unique
class MapsetTask(Enum):
    """Enumeration of possible tasks within a mapset."""

    INFO = "info"
    LOCK = "lock"
    RASTER_LAYER = "raster_layer"
    STRDS = "strds"
    VECTOR_LAYERS = "vector_layers"
    PROCESSING = "processing"
    PROCESSING_ASYNC = "processing_async"


class Mapset:
    """The main Mapset object."""

    def __init__(
        self,
        name: str,
        location_name: str,
        actinia: Actinia,
        auth: tuple,
    ) -> None:
        """Initialize the Mapset object."""
        self.name = name
        self.projection = None
        self.region = None
        self.__location_name = location_name
        self.__actinia = actinia
        self.__auth = auth
        self.raster_layers = None
        self.vector_layers = None
        self.strds = None

    def __request_url(
        actinia_url: str,  # NOQA: N805
        location_name: str,
        mapset_name: str | None = None,
        task: Enum | None = None,
    ) -> str:
        """Provide the url to an Actinia mapset resource.

        Parameters
        ----------
        actinia_url : str
            The base url to actinia server
        location_name : str
            The GRASS location name
            route: /locations/{location_name}/mapsets
        mapset_name : str, default=None
            The mapset name
            route: /locations/{location_name}/mapsets/{mapset_name}
        task : Enum(MapsetTask), default=None
            The requested task
            (info) route:
                /locations/{location_name}/mapsets/{mapset_name}/info
            (lock) route:
                /locations/{location_name}/mapsets/{mapset_name}/lock
            (raster_layers) route:
                /locations/{location_name}/mapsets/{mapset_name}/raster_layers
            (vector_layers) route:
                /locations/{location_name}/mapsets/{mapset_name}/vector_layers
            (strds) route:
                /locations/{location_name}/mapsets/{mapset_name}/strds
            (processing) route:
                /locations/{location_name}/mapsets/{mapset_name}/processing
            (processing_async) route:
                /locations/{location_name}/mapsets/{mapset_name}/processing_async

        Returns
        -------
        base_url : str
            Return the url scheme for the mapset request

        """
        base_url = f"{actinia_url}/locations/{location_name}/mapsets"
        if mapset_name is not None:
            base_url = f"{base_url}/{mapset_name}"
            if isinstance(task, MapsetTask):
                base_url = f"{base_url}/{task.value}"
        return base_url

    def info(self) -> dict:
        """Get mapset info.

        Returns
        -------
        info : dict with mapset info

        """
        if self.projection is None or self.region is None:
            proc_res = self.request_info(
                self.name,
                self.__location_name,
                self.__actinia,
                self.__auth,
            )
            self.projection = proc_res["projection"]
            self.region = Region(**proc_res["region"])
        return {"projection": self.projection, "region": self.region}

    def delete(self) -> None:
        """Delete the mapset."""
        self.delete_mapset_request(
            self.name,
            self.__location_name,
            self.__actinia,
            self.__auth,
        )
        del self.__actinia.locations[self.__location_name].mapsets[self.name]

    @classmethod
    def list_mapsets_request(
        cls,
        location_name: str,
        actinia: Actinia,
        auth: tuple,
    ) -> dict:
        """List mapsets within a location.

        Parameters
        ----------
        location_name : str
            The name of the location where the mapsets are located.
        actinia : Actinia
            An Actinia instance containing the url
        auth :
            Actinia authentication

        Returns
        -------
        mapsets : dict[mapset_name, Mapset]
            A dict of with keys equal to the mapset name and
            values set to the Mapset class instance.

        """
        url = cls.__request_url(actinia.url, location_name)
        mapset_names = request_and_check(
            "GET",
            url,
            auth=auth,
            timeout=actinia.timeout,
        )["process_results"]
        return {
            mname: Mapset(mname, location_name, actinia, auth) for mname in mapset_names
        }

    @classmethod
    def create_mapset_request(
        cls,
        mapset_name: str,
        location_name: str,
        actinia: Actinia,
        auth: tuple,
    ) -> Mapset:
        """Create a mapset within a location.

        Parameters
        ----------
        mapset_name : str
            The name of the created mapset.
        location_name : str
            The name of the location where the mapset is created
        actinia : Actinia
            An Actinia instance containing the url
        auth :
            Actinia authentication

        Returns
        -------
        Mapset
            A new mapset instance for the created mapset

        """
        # check if mapset exists
        existing_mapsets = cls.list_mapsets_request(location_name, actinia, auth)
        if mapset_name in existing_mapsets:
            log.warning(f"Mapset <{mapset_name}> already exists.")
            return existing_mapsets[mapset_name]

        url = cls.__request_url(actinia.url, location_name, mapset_name)
        request_and_check("POST", url, auth=(auth), timeout=actinia.timeout)
        return Mapset(mapset_name, location_name, actinia, auth)

    @classmethod
    def delete_mapset_request(
        cls,
        mapset_name: str,
        location_name: str,
        actinia: Actinia,
        auth: tuple,
    ) -> None:
        """Delete a mapset within a location.

        Parameters
        ----------
        mapset_name : str
            The name of the mapset to delete
        location_name : str
            The name of the mapset's location
        actinia : Actinia
            An Actinia instance containing the url
        auth :
            Actinia authentication

        """
        # check if mapset exists
        existing_mapsets = cls.list_mapsets_request(location_name, actinia, auth)
        if mapset_name not in existing_mapsets:
            log.warning(f"Mapset <{mapset_name}> does not exist and cannot be deleted.")
            return

        url = cls.__request_url(actinia.url, location_name, mapset_name)
        request_and_check("DELETE", url, auth=(auth), timeout=actinia.timeout)
        return

    @classmethod
    def request_info(
        cls,
        mapset_name: str,
        location_name: str,
        actinia: Actinia,
        auth: tuple,
    ) -> dict:
        """Get detailed info about a mapset.

        Parameters
        ----------
        mapset_name : str
            The name of mapset.
        location_name : str
            The name of the location
        actinia : Actinia
            An Actinia instance containing the url
        auth :
            Actinia authentication

        Returns
        -------
        dict
        Returns JSON process results if successful.

        """
        url = cls.__request_url(
            actinia.url,
            location_name,
            mapset_name,
            MapsetTask.INFO,
        )
        return request_and_check(
            "GET",
            url,
            auth=(auth),
            timeout=actinia.timeout,
        )["process_results"]

    def __request_raster_layers(self) -> None:
        """Request the raster layers in the mapset."""
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/raster_layers"
        )
        raster_names = request_and_check(
            "GET",
            url,
            auth=self.__auth,
            timeout=self.__actinia.timeout,
        )["process_results"]
        rasters = {
            mname: Raster(
                mname,
                self.__location_name,
                self.name,
                self.__actinia,
                self.__auth,
            )
            for mname in raster_names
        }
        self.raster_layers = rasters

    def get_raster_layers(self, *, force: bool = False) -> dict:
        """Return raster layers of the mapset.

        Parameters
        ----------
        force : bool
            Force reloading of raster layers of the mapset.

        Returns
        -------
            dict: A dict of the vector maps

        """
        if self.raster_layers is None or force is True:
            self.__request_raster_layers()
        return self.raster_layers

    def __request_vector_layers(self) -> None:
        """Request the vector layers in the mapset."""
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/vector_layers"
        )
        vector_names = request_and_check(
            "GET",
            url,
            auth=self.__auth,
            timeout=self.__actinia.timeout,
        )["process_results"]
        vectors = {
            mname: Vector(
                mname,
                self.__location_name,
                self.name,
                self.__actinia,
                self.__auth,
            )
            for mname in vector_names
        }
        self.vector_layers = vectors

    def get_vector_layers(self, *, force: bool = False) -> dict:
        """Return vector layers of the mapset.

        Parameters
        ----------
        force: bool
            Force update of vector layer dict

        Returns
        -------
            dict: A dict of the vector maps

        """
        if self.vector_layers is None or force is True:
            self.__request_vector_layers()
        return self.vector_layers

    def upload_raster(self, layer_name: str, tif_file: str) -> None:
        """Upload GTiff as a raster layer.

        Parameters
        ----------
        layer_name: string
            Name for the raster layer to create
        tif_file: string
            Path of the GTiff file to upload

        Raises
        ------
        RuntimeError:
            Error string with response status code
            and text if request fails.

        """
        files = {"file": (tif_file, Path(tif_file).open("rb"))}  # NOQA: SIM115
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/raster_layers/{layer_name}"
        )
        resp_dict = request_and_check(
            "POST",
            url,
            auth=self.__auth,
            files=files,
            timeout=self.__actinia.timeout,
        )
        job = Job(
            f"raster_upload_{self.__location_name}_{self.name}_{layer_name}",
            self.__actinia,
            self.__auth,
            resp_dict,
        )
        job.poll_until_finished()
        if job.status != "finished":
            msg = f"{job.status}: {job.message}"
            raise RuntimeError(msg)
        if self.raster_layers is None:
            self.get_raster_layers()
        self.raster_layers[layer_name] = Raster(
            layer_name,
            self.__location_name,
            self.name,
            self.__actinia,
            self.__auth,
        )

    def delete_raster(self, layer_name: str) -> None:
        """Delete a raster layer.

        Parameters
        ----------
        layer_name: str
            Name of the raster layer to delete

        """
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/raster_layers/{layer_name}"
        )
        request_and_check(
            "DELETE",
            url,
            auth=self.__auth,
            timeout=self.__actinia.timeout,
        )
        if self.raster_layers is None:
            self.get_raster_layers()
        else:
            del self.raster_layers[layer_name]
        log.info(f"Raster <{layer_name}> successfully deleted")

    def upload_vector(self, layer_name: str, vector_file: str) -> None:
        """Upload vector file (GPKG, zipped Shape, GeoJSON) as a vector layer.

        Parameters
        ----------
        layer_name: string
            Name for the vector layer to create
        vector_file: string
            Path of the GPKG/zipped Shapefile or GeoJSON to upload

        Raises
        ------
        RuntimeError
            RuntimeError string with response status code
            and text if request fails.

        """
        files = {"file": (vector_file, Path(vector_file).open("rb"))}  # NOQA: SIM115
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/vector_layers/{layer_name}"
        )
        resp_dict = request_and_check(
            "POST",
            url,
            files=files,
            auth=self.__auth,
            timeout=self.__actinia.timeout,
        )
        job = Job(
            f"vector_upload_{self.__location_name}_{self.name}_{layer_name}",
            self.__actinia,
            self.__auth,
            resp_dict,
        )
        job.poll_until_finished()
        if job.status != "finished":
            msg = f"{job.status}: {job.message}"
            raise RuntimeError(msg)
        if self.vector_layers is None:
            self.get_vector_layers()
        self.vector_layers[layer_name] = Vector(
            layer_name,
            self.__location_name,
            self.name,
            self.__actinia,
            self.__auth,
        )

    def delete_vector(self, layer_name: str) -> None:
        """Delete a vector layer.

        Parameters
        ----------
        layer_name: string
            Name of the vector layer to delete

        """
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/vector_layers/{layer_name}"
        )
        request_and_check(
            "DELETE",
            url,
            auth=self.__auth,
            timeout=self.__actinia.timeout,
        )
        if self.vector_layers is None:
            self.get_vector_layers()
        else:
            del self.vector_layers[layer_name]
        log.info(f"Vector <{layer_name}> successfully deleted")

    def __request_strds(self) -> None:
        """Request the SpaceTimeRasterDatasets in the mapset."""
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/strds"
        )
        resp = request_and_check("GET", url, auth=self.__auth)
        strds_names = resp["process_results"]
        strds = {
            sname: SpaceTimeRasterDataset(
                sname,
                self.__location_name,
                self.name,
                self.__actinia,
                self.__auth,
            )
            for sname in strds_names
        }
        self.strds = strds

    def __check_strds_existence(self, strds_name: str) -> None:
        """Check if a SpaceTimeRasterDataset exists in the mapset.

        Parameters
        ----------
        strds_name: string
            Name of the STRDS to check

        Raises
        ------
        RuntimeError
            Error if mapset does not exist.

        """
        if self.strds is None:
            self.__request_strds()
        if strds_name not in self.strds:
            msg = f"SpaceTimeRasterDataset <{strds_name}> does not exist"
            raise RuntimeError(msg)

    def get_strds(self, *, force: bool = False) -> list[SpaceTimeRasterDataset]:
        """Return SpaceTimeRasterDatasets of the given mapsets.

        Parameters
        ----------
        force: bool
            Force reload of SpaceTimeRasterDatasets

        Returns
        -------
            dict[SpaceTimeRasterDataset: str]: A dict with the SpaceTimeRasterDatasets

        """
        if self.strds is None or force is True:
            self.__request_strds()
        return self.strds

    def create_strds(
        self,
        strds_name: str,
        title: str,
        description: str,
        temporal_type: str = "absolute",
        *,
        overwrite: bool = False,
    ) -> None:
        """Return SpaceTimeRasterDatasets of the given mapsets.

        Parameters
        ----------
        strds_name: string
            Name of the STRDS to create
        title: string
            Title of the STRDS to create
        description: string
            Description of the STRDS to create
        temporal_type: string
            Temporal type of the STRDS to create
        overwrite: bool
            Allow overwriting of existing SpaceTimeRasterDatasets

        Raises
        ------
        ValueError:
            ValueError for invalid input.
        RuntimeError:
            RuntimeError if STRDS already exists and overwrite is False.

        """
        if temporal_type not in {"absolute", "relative"}:
            msg = "temporal_type must be 'absolute' or 'relative'."
            raise ValueError(msg)
        if self.strds is None:
            self.__request_strds()
        if strds_name:
            if strds_name in self.strds and not overwrite:
                msg = f"SpaceTimeRasterDataset <{strds_name}> already exists."
                raise RuntimeError(msg)
            log.info(f"Overwriting STRDS <{strds_name}>")
            self.delete_strds(strds_name)
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/strds/{strds_name}"
        )

        postkwargs = {
            "headers": self.__actinia.headers,
            "auth": self.__auth,
            "timeout": self.__actinia.timeout,
            "data": json.dumps(
                {
                    "title": title,
                    "description": description,
                    "temporal_type": temporal_type,
                },
            ),
        }
        request_and_check("POST", url, **postkwargs)

    def delete_strds(self, strds_name: str) -> None:
        """Delete a SpaceTimeRasterDataset (STRDS)."""
        self.__check_strds_existence(strds_name)
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/strds/{strds_name}"
        )
        request_and_check("DELETE", url, auth=self.__auth)
        del self.strds[strds_name]
        log.info(f"SpaceTimeRasterDataset <{strds_name}> successfully deleted")

    def sample_strds(
        self,
        strds_name: str,
        points: list[list[str]] | dict | Path | str,
        *,
        async_request: bool = False,
    ) -> dict | Job:
        """Sample SpaceTimeRasterDataset at point locations.

        Parameters
        ----------
        strds_name: str
            Name of the SpaceTimeRasterDataset to sample
        points: list[tuple] | dict | Path | str
            Point locations to sample
        async_request: bool
            If True, the request is sent asynchronously

        Returns
        -------
            dict | Job

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
        self.__check_strds_existence(strds_name)
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/strds/{strds_name}"
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
        strds_name: str,
        polygon: dict | Path | str,
        timestamp: Optional(datetime) = None,
        *,
        async_request: bool = False,
    ) -> dict:
        """Compute SpaceTimeRasterDataset statistics within polygon.

        Parameters
        ----------
        strds_name: str
            Name of the SpaceTimeRasterDatasetto compute statistics for
        polygon: list[tuple] | dict | Path | str
            Polygon to compute statistics for
        timestamp: datetime | None
            Timestamp to compute statistics for
        async_request: bool
            If True, the request is sent asynchronously

        Returns
        -------
            dict: Statistics of the SpaceTimeRasterDataset

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
        self.__check_strds_existence(strds_name)
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/strds/{strds_name}"
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

    def create_processing_job(self, pc: str | dict, name: Optional(str) = None) -> Job:
        """Create a processing job with a given processing chain.

        Parameters
        ----------
        name: str | None
            Name of the processing job (optional)
        pc: str | dict
            The actinia processing chain

        Returns
        -------
        Job

        Raises
        ------
        TypeError
            TypeError if 'pc' is invalid type.

        """
        # set name
        orig_name, name = set_job_names(name)
        # set endpoint in url
        url = (
            f"{self.__actinia.url}/locations/{self.__location_name}/"
            f"mapsets/{self.name}/processing_async"
        )
        # make POST request
        postkwargs = {
            "headers": self.__actinia.headers,
            "auth": self.__auth,
            "timeout": self.__actinia.timeout,
        }
        if isinstance(pc, str):
            if Path(pc).exists():
                postkwargs["data"] = Path(pc).read_text(encoding="UTF8")
            else:
                postkwargs["data"] = pc
        elif isinstance(pc, dict):
            postkwargs["data"] = json.dumps(pc)
        else:
            msg = "Given process chain has no valid type."
            raise TypeError(msg)

        resp = request_and_check("POST", url, **postkwargs)
        # create a job
        job = Job(orig_name, self.__actinia, self.__auth, resp)
        self.__actinia.jobs[name] = job
        return job


# TODO: # NOQA: FIX002, TD002, TD003
# * /locations/{location_name}/mapsets/{mapset_name}/processing - POST
# * /locations/{location_name}/mapsets/{mapset_name}/processing_async - POST
# * /locations/{location_name}/mapsets/{mapset_name}/lock - GET, DELETE, POST
# * /locations/{location_name}/mapsets/{mapset_name}/raster_layers - DELETE, PUT
# * /locations/{location_name}/mapsets/{mapset_name}/strds - GET
# * /locations/{location_name}/mapsets/{mapset_name}/vector_layers
