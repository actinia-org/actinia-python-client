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

Upload a GTif as raster layers to a user mapset (here the user mapset will be
created before)
```
# TODO add mapset creation
mapset_name = "AW_raster_upload"
# upload tif
raster_layer_name = "test"
file = "~/data/tif/elevation.tif"
mapsets["PERMANENT"]
locations["nc_spm_08"].mapsets[mapset_name].upload_raster(raster_layer_name, file)
```

Delete a raster layer
```
locations["nc_spm_08"].mapsets[mapset_name].delete_raster(raster_layer_name)
# TODO delete mapset
```
