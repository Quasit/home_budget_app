from setuptools import find_packages, setup

setup(
    name='home_budget',
    version='1.0.0',
    packages=find_packages(exclude="tests"),
    include_package_data=True,
    install_requires=[
        'flask',
        'sqlalchemy',
    ],
)
