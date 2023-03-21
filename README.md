https://levelup.gitconnected.com/how-to-deploy-a-cython-package-to-pypi-8217a6581f09

# PRE-COMMIT

pre-commit install

pre-commit migrate-config

pre-commit run --all-files


# BUILD

python setup.py sdist bdist_wheel

python -m twine upload --repository pypi dist/*