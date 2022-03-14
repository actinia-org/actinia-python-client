# Dev setup for the actinia-python-client library development

Setup virtural env
```
python3 -m venv env
source env/bin/activate
```
With `deactivate` you can exit the virtual env

## Install actinia for development
```
make installdev
```
Test with Python3:
```python3
from actinia import Actinia
test = Actinia()
```

## Run tests
```
make test
```
