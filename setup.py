from setuptools import setup, find_packages

with open("README.md", "r") as longdesc:
    long_description = longdesc.read()

setup(
    name='tagesschauscraper',
    version='0.1.0',
    description='A library for scraping the German news archive of Tagesschau.de',
    long_description=long_description,
    url='https://github.com/TheFerry10/TagesschauScraper',
    author='Malte Sauerwein',
    author_email='malte.sauerwein@live.de',
    license='GPL-3.0 license',
    keywords='tagesschau scraper scraping news archive',
    packages=find_packages(),
    install_requires=[
        "pytest",
        "requests",
        "beautifulsoup4",
    ],
    project_urls={
        'Bug Reports': 'https://github.com/TheFerry10/tagesschauscraper/issues',
        'Source': 'https://github.com/TheFerry10/tagesschauscraper',
    },
)