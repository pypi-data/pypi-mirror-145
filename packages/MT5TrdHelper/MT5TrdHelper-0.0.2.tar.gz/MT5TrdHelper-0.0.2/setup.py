from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Python MT5 trade helpers'
LONG_DESCRIPTION = 'This package is a wrapper on Mt5 python module'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="MT5TrdHelper",
    version=VERSION,
    author="Nazrul Islam",
    author_email="nazrulgithub@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    # add any additional packages that
    install_requires=['pandas', 'python-dateutil', 'pymt5adapter',
                      'localconfig'],
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'mt5 python', 'mt5 python algotrading',
              'forex algotrading', 'forex python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)
