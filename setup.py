# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
    name='ege_django_auth_jwt',
    packages=['ege_django_auth_jwt', ],
    version='1.2.1',
    download_url='https://github.com/CoticEaDIFRN/ege_django_auth_jwt/releases/tag/1.2.1',
    description='EGE JWT authentication for Django',
    author='Kelson da Costa Medeiros',
    author_email='kelson.medeiros@ifrn.edu.br',
    url='https://github.com/CoticEaDIFRN/ege_django_auth_jwt',
    keywords=['EGE', 'JWT', 'Django', 'Auth', 'SSO', 'client', ],
    install_requires=['PyJWT==1.7.1', 'requests-2.21.0'],
    classifiers=[]
)

