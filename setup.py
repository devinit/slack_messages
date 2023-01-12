from setuptools import setup, find_packages

setup(name='slack_messages',
      version='0.1',
      packages=find_packages(),
      install_requires=('slack_sdk>=3.13.0','jinja2'),
      )
