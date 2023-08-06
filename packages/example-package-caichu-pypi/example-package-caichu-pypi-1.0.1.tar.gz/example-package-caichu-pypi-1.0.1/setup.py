from setuptools import setup

setup(
   name='example-package-caichu-pypi',
   version='1.0.1',
   description='A useful module',
   author='Cai Chu',
   author_email='caichu.fh@antgroup.com',
   packages=['example_package'],  #same as name
   install_requires=['wheel', 'bar'], #external packages as dependencies,
   platforms=["any"]
)
