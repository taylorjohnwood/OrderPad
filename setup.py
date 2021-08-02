from distutils.core import setup
from setuptools import find_packages

NAME = 'Taylor J Wood'
EMAIL = 'taylorjohnwood@gmail.com'

setup(
    name='OrderPad',
    version='2.0',
    description='Scrape Commsec for market order positions and generate a spreadsheet',
    author=NAME,
    author_email=EMAIL,
    maintainer=NAME,
    maintainer_email = EMAIL,
    packages=find_packages(),
    package_data={
        "gui":['resources/*'],
        "backend":['resources/*']
    },
    include_package_data=True,
    scripts=['startOrderPad.py'],
    install_requires=['PyQt5', 'openpyxl', 'beautifulsoup4']
)