#!/bin/sh

pep8 -r --show-pep8 sdk

pylint -r n sdk

nosetests --with-coverage --cover-erase --cover-package sdk
