import os
from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fn:
        return fn.read()

setup(
    name='nsx-vmc-aws-integration-python-sdk',
    version='0.0.1',
    description='nsx-vmc-aws-integration-python-sdk',
    long_description=read('README.rst'),
    license=read('LICENSE.txt'),
    author='VMware, Inc.',
    url='https://github.com/vmware/vsphere-automation-sdk-python',
)