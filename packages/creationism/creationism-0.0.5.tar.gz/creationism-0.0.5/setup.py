from setuptools import setup, find_packages

setup(
    name='creationism',
    version='0.0.5',
    author='Mart van Rijthoven',
    author_email='mart.vanrijthoven@gmail.com',
    packages=find_packages(exclude=("tests",'notebooks')),
    url='http://pypi.python.org/pypi/creationism/',
    license='LICENSE.txt',
    long_description='Creationism enables you to create like a God',
)