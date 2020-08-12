from setuptools import setup, find_namespace_packages

setup(
    name='kubemlops-logging',
    version='0.1-dev1',
    packages=find_namespace_packages(include=["kubemlops.*"]),
    author='Kaizen Team',
    author_email='kaizen-tm@microsoft.com',
    description='KubeMLOps logging support package',
    install_requires=['opencensus-ext-azure', 'opencensus-ext-logging']
)
