import os
from setuptools import setup

def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as fn:
        return fn.read()

setup(
    name='vsphere-automation-sdk',
    version='0.0.1',
    description='vsphere-automation-sdk',
    long_description=read('README.rst'),
    license=read('LICENSE.txt'),
    author='VMware, Inc.',
    url='https://github.com/vmware/vsphere-automation-sdk-python',
)