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
# TODO add mapset creation
mapset_name = "test_mapset"

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

# TODO delete mapset
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
# TODO add mapset creation
mapset_name = "test_mapset"

# upload tif
vector_layer_name = "test"
file = "/home/testuser/data/firestations.geojson"
locations["nc_spm_08"].mapsets[mapset_name].upload_vector(vector_layer_name, file)
print(locations["nc_spm_08"].mapsets[mapset_name].vector_layers.keys())
```

Delete a raster layer
```
locations["nc_spm_08"].mapsets[mapset_name].delete_vector(vector_layer_name)
print(locations["nc_spm_08"].mapsets[mapset_name].vector_layers.keys())

# TODO delete mapset
```

## STRDS management

Get all space time raster data sets (STRDS) of the `modis_lst` mapsets
```
vectors = mapsets["modis_lst"].get_strds()
print(vectors.keys())
```

Get information of the STRDS `LST_Day_monthly`
```
info = vectors["LST_Day_monthly"].get_info()
```

Create an empty STRDS and register raster in the same mapset
```
# TODO add mapset creation and add raster
mapset_name = "test_mapset"

# create STRDS
strdsname = "test_strds"
locations["nc_spm_08"].mapsets[mapset_name].create_strds(strdsname, "title", "description")
print(locations["nc_spm_08"].mapsets[mapset_name].strds.keys())

# register STRDS
raster_maps = "test_elevation1,test_elevation2"
strds.add_raster_layers(raster_maps, "1990-01-01,2000-01-01", "1990-01-02,2000-01-02")
print(locations["nc_spm_08"].mapsets[mapset_name].strds[strdsname].raster_layers.keys())
```

Unregister raster maps from STRDS
```
strds.remove_raster_layers(raster_maps.split(",")[0])
print(locations["nc_spm_08"].mapsets[mapset_name].strds[strdsname].raster_layers.keys())
```

Delete a STRDS
```
locations["nc_spm_08"].mapsets[mapset_name].delete_strds(strdsname)
print(locations["nc_spm_08"].mapsets[mapset_name].strds.keys())

# TODO delete mapset
```
