from setuptools import setup
from setuptools import setup, find_packages

setup(name='slack_hero',
      version='0.2.2',
      packages=find_packages(),
      python_requires=">=3.6",
      install_requires=('slack_sdk>=3.13.0',),
      url='https://github.com/devinit/slack_messages',
      )
