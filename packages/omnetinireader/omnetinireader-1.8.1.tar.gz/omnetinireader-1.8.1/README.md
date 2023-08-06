# omnet-file-reader

This Python repository provides a file reader for input files (*.ini) for the OMNeT++ simulation framework.

```
python3 setup.py sdist bdist_wheel
twine check dist/*
twine upload --verbose --repository testpypi dist/*
twine upload --verbose dist/*
```
