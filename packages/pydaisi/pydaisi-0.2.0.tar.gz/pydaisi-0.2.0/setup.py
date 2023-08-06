import setuptools

setuptools.setup(
    version='0.2.0',
    license='Apache License 2.0',
    url='https://github.com/BelmontTechnology/PyDaisi',
    keywords='Daisi SDK',
    install_requires=[
     'requests',
     'python-dotenv',
     'dill',
     'rich'
    ],
    packages=setuptools.find_packages(),
    include_package_data=True,
    python_requires='>=3.8'
)
