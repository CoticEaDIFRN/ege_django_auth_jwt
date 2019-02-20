#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "NAME
       release

SYNOPSIS
       ./release.sh [-d|-p|-g] <version>

DESCRIPTION
       Create a new release to ege_utils python package.

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
    name='ege_utils',
    description='Utils classes for EGE project',
    long_description='Utils classes for EGE project',
    license='MIT',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@gmail.com',
    packages=['ege_utils', 'ege_utils/templates'],
    include_package_data=True,
    version='$1',
    download_url='https://github.com/CoticEaDIFRN/ege_utils/releases/tag/$1',
    url='https://github.com/CoticEaDIFRN/ege_utils',
    keywords=['EGE', 'JWT', 'Django', 'Auth', 'SSO', 'client', ],
    install_requires=['PyJWT==1.7.1', 'requests==2.21.0', 'django>=2.0,<3.0'],
    classifiers=[]
)
""" > setup.py
    docker build -t ifrn/ege.utils --force-rm .
    docker run --rm -it -v `pwd`:/src ifrn/ege.utils python setup.py sdist
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
        docker run --rm -it -v `pwd`:/src ifrn/ege.utils twine upload dist/ege_utils-$2.tar.gz
    fi
fi

echo ""
echo "Done."
