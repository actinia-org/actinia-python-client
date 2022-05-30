# Process Chain Validation

A process chain can be validated before a job is started.

First connecting actinia Python library with [actinia](https://actinia.mundialis.de/) and set authentication:
```
from actinia import Actinia

actinia_mundialis = Actinia()
actinia_mundialis.get_version()
actinia_mundialis.set_authentication("demouser", "gu3st!pa55w0rd")

# request all locations
locations = actinia_mundialis.get_locations()
```

## Synchronous process chain validation
```
pc = {
    "list": [
      {
          "id": "r_mapcalc",
          "module": "r.mapcalc",
          "inputs": [
              {
                  "param": "expression",
                  "value": "elevation=42"
              }
          ]
      }
    ],
    "version": "1"
}
pc = {"list": [{"id": "r_mapcalc","module": "r.mapcalc","inputs": [{"param": "expression","value": "elevation=42"}]}],"version": "1"}
actinia_mundialis.locations["nc_spm_08"].validate_process_chain_sync(pc)
```

## Asynchronous process chain validation:
```
pc = {
    "list": [
      {
          "id": "r_mapcalc",
          "module": "r.mapcalc",
          "inputs": [
              {
                  "param": "expression",
                  "value": "elevation=42"
              }
          ]
      }
    ],
    "version": "1"
}
pc = {"list": [{"id": "r_mapcalc","module": "r.mapcalc","inputs": [{"param": "expression","value": "elevation=42"}]}],"version": "1"}
val_job = actinia_mundialis.locations["nc_spm_08"].validate_process_chain_async(pc)
val_job.poll_until_finished()
print(val_job.status)
print(val_job.message)
```
