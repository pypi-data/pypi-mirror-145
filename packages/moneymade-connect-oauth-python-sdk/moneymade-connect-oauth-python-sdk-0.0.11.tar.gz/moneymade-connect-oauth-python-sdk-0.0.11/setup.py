from setuptools import setup
from codecs import open

with open('README.md', 'r', 'utf-8') as f:
  readme = f.read()

setup(
    name='moneymade-connect-oauth-python-sdk',
    version='0.0.11',
    description='Packages which makes simplier integration with MoneyMade OAuth feature',
    long_description=readme,
    long_description_content_type='text/markdown',
    author_email='vitalik@moneymade.io',
    packages=['moneymade_connect_python_sdk'],
    package_dir={'moneymade_connect_python_sdk': 'src/moneymade_connect_python_sdk'},
    include_package_data=True,
    python_requires=">=3.7, <4",
    install_requires=[
        'requests==2.26.0'
    ],
    project_urls={
        'Documentation': 'https://pypi.org/project/moneymade-connect-oauth-python-sdk',
        'Source': 'https://github.com/moneymadeio/moneymade-connect-python-sdk',
    }
)
