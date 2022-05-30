# Location Management

With the location management the locations can be requested as well as
information of each location. Also a location can be created and deleted if the user is permitted.

First connecting actinia Python library with [actinia](https://actinia.mundialis.de/) and
set authentication (Attention: The demouser is not permitted to create or delete a location!)
```
from actinia import Actinia

actinia_mundialis = Actinia()
actinia_mundialis.get_version()
actinia_mundialis.set_authentication("demouser", "gu3st!pa55w0rd")
```

## Get locations and locaton information of a special location:
```
locations = actinia_mundialis.get_locations()
print(locations.keys())
locations["nc_spm_08"].get_info()
# or
actinia_mundialis.locations["nc_spm_08"].get_info()
```

## Create a new location
```
new_location = actinia_mundialis.create_location("test_location", 25832)
print(new_location.name)
print(new_location.region)
print([loc for loc in actinia_mundialis.locations])
```

## Delete a location
```
actinia_mundialis.locations["test_location"].delete()
print([loc for loc in actinia_mundialis.locations()])
```
