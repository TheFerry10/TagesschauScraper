from setuptools import setup, find_packages
from tagesschauscraper import __version__


with open("README.rst", "r") as longdesc:
    long_description = longdesc.read()
    
required_packaes = [
        "requests==2.28.2",
        "beautifulsoup4==4.11.1",
    ]

setup(
    name='tagesschauscraper',
    version=__version__,
    description='A library for scraping the German news archive of Tagesschau.de',
    long_description=long_description,
    url='https://github.com/TheFerry10/TagesschauScraper',
    author='Malte Sauerwein',
    author_email='malte.sauerwein@live.de',
    license='GPL-3.0 license',
    keywords='tagesschau scraper scraping news archive',
    packages=find_packages(),
    install_requires=required_packaes,
    project_urls={
        'Bug Reports': 'https://github.com/TheFerry10/tagesschauscraper/issues',
        'Source': 'https://github.com/TheFerry10/tagesschauscraper',
    },
)