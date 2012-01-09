from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages


setup(
    name='gevent-selfpipe',
    version='0.0.3',
    description='Hack to enable gevent-based scheduling of blocking calls.',
    author='Zachary Voase',
    author_email='z@zacharyvoase.com',
    url='http://github.com/zacharyvoase/gevent-selfpipe',
    packages=find_packages(where='lib'),
    package_dir={'': 'lib'},
    install_requires=[
        'gevent>=0.13.6',
    ],
)
