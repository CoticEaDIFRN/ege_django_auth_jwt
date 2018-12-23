#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "NAME
       release

SYNOPSIS
       ./release.sh [-d|-p|-g] <version>

DESCRIPTION
       Create a new release to ege_django_auth_jwt python package.

OPTIONS
       -d         Deploy to Github and PyPI
       -p         Deploy to PyPI
       -g         Deploy to Github
       <version>  Release version number

EXAMPLES
       o   Build to local usage only:
                  ./release.sh 1.1
       o   Build and deploy to both Github and PyPI:
                  ./release.sh -d 1.1
       o   Build and deploy to PyPI only:
                  ./release.sh -p 1.1
       o   Build and deploy to Github only:
                  ./release.sh -g 1.1
"
fi


create_setup_cfg_file() {
    echo """# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
    name='ege_django_auth_jwt',
    packages=['ege_django_auth_jwt', ],
    version='$1',
    download_url='https://github.com/CoticEaDIFRN/ege_django_auth_jwt/releases/tag/$1',
    description='JWT authentication for Django from EGE project',
    long_description='JWT authentication for Django EGE project',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@ifrn.edu.br',
    url='https://github.com/CoticEaDIFRN/ege_django_auth_jwt',
    keywords=['EGE', 'JWT', 'Django', 'Auth', 'SSO', 'client', ],
    install_requires=['PyJWT==1.7.1', 'requests==2.21.0', 'django>=2.0,<3.0'],
    classifiers=[]
)
""" > setup.py
    docker build -t ifrn/ege.django_auth_jwt --force-rm .
    docker run --rm -it -v `pwd`:/src ifrn/ege.django_auth_jwt python setup.py sdist
}

if [[ $# -eq 1 ]]
  then
    echo "Build to local usage only. Version: $1"
    echo ""
    create_setup_cfg_file $1
fi

if [[ $# -eq 2 ]] && [[ "$1" == "-d" || "$1" == "-g" || "$1" == "-p" ]]
  then
    echo "Build to local. Version: $2"
    echo ""
    create_setup_cfg_file $2

    if [[ "$1" == "-d" || "$1" == "-g" ]]
      then
        echo ""
        echo "GitHub: Pushing"
        echo ""
        git add setup.py
        git commit -m "Release $2"
        git tag $2
        git push --tags origin master
    fi

    if [[ "$1" == "-d" || "$1" == "-p" ]]
      then
        echo ""
        echo "PyPI Hub: Uploading"
        echo ""
        docker run --rm -it -v `pwd`:/src ifrn/ege.django_auth_jwt twine upload dist/ege_django_auth_jwt-$2.tar.gz
    fi
fi

echo ""
echo "Done."
