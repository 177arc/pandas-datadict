import pathlib
from setuptools import setup

# The directory containing this file
cwd = pathlib.Path(__file__).parent

# The text of the README file
readme = (cwd / 'README.md').read_text()

# This call to setup() does all the work
setup(name='pandas-datadict',
        version='0.2.3',
        description='Data dictionary functionality for pandas data frames',
        long_description=readme,
        long_description_content_type='text/markdown',
        url='https://github.com/177arc/pandas-datadict',
        author='Marc Maier',
        author_email='py@177arc.net',
        license='MIT',
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
        ],
        packages=['datadict', 'datadict.jupyter'],
        include_package_data=True,
        install_requires=['pandas>=0.19', 'openpyxl']
)