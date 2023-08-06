#!/usr/bin/env python


from setuptools import setup, find_packages
# from pip.req import parse_requirements
try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

from camillademo import __version__


def get_reqs():
    install_reqs = parse_requirements('requirements.txt')
    return [str(ir.req) for ir in install_reqs]


setup(
    name='camillademo',
    version=__version__,
    description='A python demo',
    author='camillalo',
    author_email='2246223018@qq.com',
    license='MIT License',
    url='https://gitee.com/camilla/python-demo-20220408',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'six>=1.9.0',
    ],
    extras_require={
        'dev': [
            'prospector>=0.10.2',
        ],
        'test': [
            'coverage>=3.7.1',
            'coveralls>=0.5',
            'pytest>=7.1.1',
            'python-coveralls>=2.5.0',
        ],
        'docs': [
            'Sphinx>=1.3.1',
        ],
    },
    # test_suite='nose.collector',
)
