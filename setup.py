# -*- coding: utf-8 -*-
from distutils.core import setup
setup(
    name='ege_auth_jwt',
    packages=['ege_auth_jwt', ],
    version='1.1.1',
    download_url='https://github.com/CoticEaDIFRN/ege_auth_jwt/releases/tag/1.1.1',
    description='JWT authentication for Django from EGE project',
    long_description='JWT authentication for Django EGE project',
    author='Kelson da Costa Medeiros',
    author_email='kelsoncm@ifrn.edu.br',
    url='https://github.com/CoticEaDIFRN/ege_auth_jwt',
    keywords=['EGE', 'JWT', 'Django', 'Auth', 'SSO', 'client', ],
    install_requires=['PyJWT==1.7.1', 'requests==2.21.0', 'django>=2.0,<3.0'],
    classifiers=[]
)

