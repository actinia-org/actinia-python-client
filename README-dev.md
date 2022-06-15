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
make devtest
```
To run only a few tests you can mark the tests for development with
`@pytest.mark.dev` and add `import pytest` to the `.py` file/s with the tests
you want to run. Then run
```
make devtest
```
(This fails if no test is marked!)
