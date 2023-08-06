# Packaging instructions

Change the Indago version in `setup.py`.

Remove old files:
```bash
rm -r build dist Indago.egg-info
```

Build:
```bash
/opt/anaconda3/bin/python setup.py clean sdist bdist_wheel
```

Upload to TestPyPI:
```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

Upload to PyPI:
```bash
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
