
pep8 -r --show-pep8 sdk

pylint -i y -r n sdk

nosetests --with-coverage --cover-erase --cover-package sdk