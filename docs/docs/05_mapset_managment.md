# Mapsets Management

With the mapset management the mapsets of a specified location can be
requested as well as information of each mapset.
Also a mapsest can be created and deleted if the user is permitted.

First connecting actinia Python library with [actinia](https://actinia.mundialis.de/) and set authentication (Attention: The demouser is not permitted to create or delete a mapset!)
```
from actinia import Actinia

actinia_mundialis = Actinia()
actinia_mundialis.get_version()
actinia_mundialis.set_authentication("demouser", "gu3st!pa55w0rd")

# request all locations
locations = actinia_mundialis.get_locations()
```

## Get Mapsets of Specified Location
Get mapsets of the ***nc_spm_08*** location:
```
mapsets = actinia_mundialis.locations["nc_spm_08"].get_mapsets()
print(mapsets.keys())
```

## TODO: Create Mapset in Specified Location

## TODO: Delete Mapset in Specified Location
