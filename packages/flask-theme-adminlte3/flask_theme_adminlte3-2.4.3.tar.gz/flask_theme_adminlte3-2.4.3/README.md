<!---|START introduction|--->"
# Flask-Theme-AdminLTE3

AdminLTE3 Theme integrated into Flask.

<!---|END introduction|--->"

# Publishing a New Version

### Create distribution package

The following command packages this
code into the `dist` directory

```python
pip install wheel
python setup.py sdist bdist_wheel
```

### Upload to test PyPi

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```


### Upload to PyPi

```bash
twine upload dist/*
```