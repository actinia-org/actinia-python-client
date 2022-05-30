# Processing

Start a process chain with a valid process chain.

First connect actinia Python library with [actinia](https://actinia.mundialis.de/) and set authentication:
```
from actinia import Actinia

actinia_mundialis = Actinia()
actinia_mundialis.get_version()
actinia_mundialis.set_authentication("demouser", "gu3st!pa55w0rd")

# request all locations
locations = actinia_mundialis.get_locations()
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
