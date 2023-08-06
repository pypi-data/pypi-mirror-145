from setuptools import find_packages, setup

setup(
    name='PyDeepfake',
    version='0.1.3',
    requires= ['timm',
        'fvcore',
        'albumentations',
        'kornia',
        'simplejson',
        'tensorboard',
    ],
    packages=find_packages(),
    license="apache 2.0")
