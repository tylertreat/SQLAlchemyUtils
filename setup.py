from setuptools import find_packages
from setuptools import setup

VERSION = '0.0.4'

setup_args = dict(
    name='SQLAlchemyUtils',
    description='Useful utilities for working with SQLAlchemy.',
    url='https://github.com/tylertreat/SQLAlchemyUtils',
    version=VERSION,
    license='Apache',
    packages=find_packages(),
    include_package_data=True,
    author='Tyler Treat',
    author_email='ttreat31@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
)

if __name__ == '__main__':
    setup(**setup_args)

