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


## Using toolbox
```
from actinia import toolbox

toolbox.list_mapsets("https://actinia-dev.mundialis.de/", "v3", ("demouser", "gu3st!pa55w0rd"), "nc_spm_08")

toolbox.list_mapsets("https://actinia-dev.mundialis.de/", "v3", ("demouser", "gu3st!pa55w0rd"), "nc_spm_08")["PERMANENT"].info()
```
