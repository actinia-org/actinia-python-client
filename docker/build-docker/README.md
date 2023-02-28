# README for local Build

```
docker build . -t build
docker run --rm -it -w /src/actinia-python-client -v ${HOME}/repos/actinia/actinia-python-client:/src/actinia-python-client build
```
Inside docker use the following to build the wheel:
```
python3 -m build --outdir build-pkg .
```

Test the wheel:
```
cd
pip3 install /src/actinia-python-client/build-pkg/*

python3
from actinia import Actinia
actinia_mundialis = Actinia()
actinia_mundialis.get_version()
```
