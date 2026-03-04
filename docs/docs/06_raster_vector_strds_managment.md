# Raster, Vector and STRDS Management

```
from actinia import Actinia

actinia_mundialis = Actinia()
actinia_mundialis.get_version()
actinia_mundialis.set_authentication("demouser", "gu3st!pa55w0rd")

# request all locations
locations = actinia_mundialis.get_locations()
# Get Mapsets of nc_spm_08 location
mapsets = actinia_mundialis.locations["nc_spm_08"].get_mapsets()
```

## Raster manangement

Get all rasters of the `PERMANENT` mapsets
```
rasters = mapsets["PERMANENT"].get_raster_layers()
print(rasters.keys())
```

Get information of the raster `zipcodes`
```
info = rasters["zipcodes"].get_info()
```

Upload a GTif as raster layer to a user mapset (here the user mapset will be
created before)
```
mapset_name = "test_mapset"

# mapset creation
locations["nc_spm_08"].create_mapset(mapset_name)

# upload tif
raster_layer_name = "test"
file = "/home/testuser/data/elevation.tif"
locations["nc_spm_08"].mapsets[mapset_name].upload_raster(raster_layer_name, file)
print(locations["nc_spm_08"].mapsets[mapset_name].raster_layers.keys())
```

Delete a raster layer
```
locations["nc_spm_08"].mapsets[mapset_name].delete_raster(raster_layer_name)
print(locations["nc_spm_08"].mapsets[mapset_name].raster_layers.keys())

# delete mapset
locations["nc_spm_08"].delete_mapset(mapset_name)
```

## Vector management

Get all vector maps of the `PERMANENT` mapsets
```
vectors = mapsets["PERMANENT"].get_vector_layers()
print(vectors.keys())
```

Get information of the vector `boundary_county`
```
info = vectors["boundary_county"].get_info()
```

Upload a GeoJSON as vector layer to a user mapset (here the user mapset will
be created before)
```
mapset_name = "test_mapset"

# mapset creation
locations["nc_spm_08"].create_mapset(mapset_name)

# Upload GeoJSON
vector_layer_name = "test"
file = "/home/testuser/data/firestations.geojson"
locations["nc_spm_08"].mapsets[mapset_name].upload_vector(vector_layer_name, file)
print(locations["nc_spm_08"].mapsets[mapset_name].vector_layers.keys())
```

Delete a vector layer
```
locations["nc_spm_08"].mapsets[mapset_name].delete_vector(vector_layer_name)
print(locations["nc_spm_08"].mapsets[mapset_name].vector_layers.keys())

# delete mapset
locations["nc_spm_08"].delete_mapset(mapset_name)
```

## Space-Time-Raster-Dataset (STRDS) management

Create a new, empty STRDS and register raster maps
(here the user mapset will be created before)

```
strds_name = "test_strds"

# Create mapset
mapset_name = "test_strds_mapset"
locations["nc_spm_08"].create_mapset(mapset_name)

# Create new STRDS
locations["nc_spm_08"]
    .mapsets[mapset_name]
    .create_strds(
        strds_name,
        "Title of the STRDS",
        "Longer description description of the STRDS",
        "absolute",  # temporal type of the STRDS
    )

# Create sample raster data
expression = "\n".join(f"map_{i}={i} * x()" for i in range(2)
pc = {
    "list": [
        {
            "id": "g_region_1",
            "module": "g.region",
            "flags": "p",
            "inputs": [
                {
                    "param": "raster",
                    "value": "elevation",
                    },
                    ],
            },
        {
            "id": "r_mapcalc_1",
            "module": "r.mapcalc"
            "inputs": [
                {
                    "param": "expression",
                    "value": expression,
                    },
                    ]
            },
    ],
    "version": 1,
}
locations["nc_spm_08"]
    .mapsets[mapset_name]
    .processing_async(pc)



# Register raster maps in STRDS
locations["nc_spm_08"]
    .mapsets[mapset_name]
    .strds[strds_name].register_raster_layers(
        [
            {
                "name": "map_0",
                "start_time": "1951-01-01 00:00:00",
                "end_time": "1952-01-01 00:00:00",
            },
            {
                "name": "map_1",
                "start_time": "1952-01-01 00:00:00",
                "end_time": "1953-01-01 00:00:00",
            },
            {
                "name": "map_2",
                "start_time": "1953-01-01 00:00:00",
                "end_time": "1954-01-01 00:00:00",
            },
        ],
    )
```

Get STRDS metadata and list raster maps

```
# Get general info
locations["nc_spm_08"]
    .mapsets[mapset_name]
    .strds[strds_name].get_info()

# Get selected, registered raster maps
locations["nc_spm_08"]
    .mapsets[mapset_name]
    .strds[strds_name].get_strds_raster_layers(
        where="start_time >= '1952-01-01 00:00:00'"
    )
```

Sample STRDS at point locations

```
# Define input points
points = [
    ["point_1", 1, 2,],
    ["point_2", 3, 4,],
    ]

# Run sampling
locations["nc_spm_08"]
    .mapsets[mapset_name]
    .strds[strds_name].sample_strds(
        points
    )
```

Compute univariate statistics for areas over an STRDS

```
# Define input GeoJSON
geojson = 

# Compute univariate statistics from STRDS
locations["nc_spm_08"]
    .mapsets[mapset_name]
    .strds[strds_name].compute_strds_statistics(
        geojson
    )
```

Render STRDS

```
locations["nc_spm_08"]
    .mapsets[mapset_name]
    .strds[strds_name]
    .render(
        {
            "n": ,
            "s": ,
            "e": ,
            "w": ,
            "width": 800,
            "height": 600,
            "start_time": "1952-01-01 00:00:00",
            "end_time": "1954-01-01 00:00:00",
        }
    )
```