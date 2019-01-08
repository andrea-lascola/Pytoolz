all : documentation build install lint deploy
.PHONY: all

documentation:
		cd docs && make html

build:
		rm -f dist/*
		python setup.py sdist

install:
		pip install -r requirements.txt

lint:
		flake8 --ignore=F401,F403,F811,F84,W,E1,E2,E3,E4,E5,E6,E7,E8 pytoolzs

deploy:
		twine upload -p ${PYPI_PWD} -u ${PYPI_USER} --repository-url https://upload.pypi.org/legacy/ dist/*
