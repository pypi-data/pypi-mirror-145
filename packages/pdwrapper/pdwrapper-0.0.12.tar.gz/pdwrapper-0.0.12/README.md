# pdwrapper

Platform Deployment Wrapper

This is a cli tool used within NX targets in platform, and platform-ui repos.

It is used to deploy and rollback NX apps (serverless services), as well as run migrations, sfsp and roll them back too. 
Pdwrapper handles the passing of information from one job to the other through traits.yml file for each app.

Base service traits.yml

```yaml
name: iam
type: service
deploy: true
migrations: true
sfsp: true
regions:
  - us-east-1
stages:
  - sbx
  - dev
```

Base ui traits.yml

```yaml
name: main
type: ui
deploy: true
stages:
  - sbx
  - dev
```

## Publish to PyPi

Update version in `setup.py` and `pdwrapper/__init__.py`.

### Prepare

Edit `~/.pypirc`
```
[pypi]
username = __token__
password = PYPI_API_TOKEN
```

Install requirements:

```shell
$ python3 -m pip install --upgrade pip
$ pip3 install setuptools wheel twine
```

### Build and Publish

```shell
# Clean existing build (optional)
$ rm -rf build dist pdwrapper.egg-info
# Create new build
$ python3 setup.py sdist bdist_wheel
# Deploy to PyPi
$ python3 -m twine upload --repository pypi dist/* --verbose
```
