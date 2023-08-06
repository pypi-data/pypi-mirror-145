from setuptools import setup, find_packages

install_requires = [
    'requests',
    'polling2',
    'urllib3',
    'mock',
    ]

setup(name='converterapi',
version='1.0.0',
description='Test Converter',
author='jiminlee',
author_email='jimin.lee@nota.ai',
install_requires=install_requires,
python_requires='>=3',
packages=find_packages()
)