# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['wi_voice_main']
setup_kwargs = {
    'name': 'wi-voice-main',
    'version': '0.1.0',
    'description': 'Easy voice',
    'long_description': None,
    'author': 'Willis',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
