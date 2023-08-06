from setuptools import setup
from setuptools import find_packages

setup(
    name='animal_scraper', ## This will be the name your package will be published with
    version='0.1.1', 
    description='Mock package that downloads images of animals',
    author='Ivan Ying', # Your name
    license='MIT',
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['requests', 'beautifulsoup4', 'selenium', 'webdriver_manager'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)