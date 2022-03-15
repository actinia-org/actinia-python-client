# Quickstart

Connecting actinia Python library with [actinia](https://actinia.mundialis.de/)
```
from actinia import Actinia

actinia_mundialis = Actinia()
actinia_mundialis.get_version()
```
or connect to [actinia-dev](https://actinia-dev.mundialis.de/) with version 3:
```
from actinia import Actinia

actinia_dev_mundialis = Actinia("https://actinia-dev.mundialis.de/", "v3")
actinia_dev_mundialis.get_version()
```

Set authentication to get access to the actinia functionallity
```
actinia_mundialis.set_authentication("demouser", "gu3st!pa55w0rd")
```

## Location Management
Get locations and locaton information of a special location:
```
locations = actinia_mundialis.get_locations()
print(locations.keys())
locations["nc_spm_08"].get_info()
```

## Mapsets mManagement
Get mapsets of the ***nc_spm_08*** location:
```
mapsets = actinia_mundialis.locations["nc_spm_08"].get_mapsets()
print(mapsets.keys())
```

## Ephemeral Processing
Start an ephemeral processing job
```
pc = {
    "list": [
      {
          "id": "r_mapcalc",
          "module": "r.mapcalc",
          "inputs": [
              {
                  "param": "expression",
                  "value": "baum=5"
              }
          ]
      }
    ],
    "version": "1"
}
job = actinia_mundialis.locations["nc_spm_08"].create_processing_export_job(pc, "test")
job.poll_until_finished()

print(job.status)
print(job.message)
```
