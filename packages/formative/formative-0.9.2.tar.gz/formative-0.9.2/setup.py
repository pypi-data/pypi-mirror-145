# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['formative',
 'formative.admin',
 'formative.filetype',
 'formative.forms',
 'formative.migrations',
 'formative.models',
 'formative.stock',
 'formative.templatetags']

package_data = \
{'': ['*']}

install_requires = \
['django-admin-inline-paginator',
 'django-better-admin-arrayfield>=1.4.2,<2.0.0',
 'django-environ',
 'django-jazzmin',
 'django-localflavor>=3.1,<4.0',
 'django-polymorphic',
 'django-webpack-loader',
 'django-widget-tweaks',
 'django>=4.0,<5.0',
 'ffmpeg-python',
 'gunicorn',
 'markdown',
 'markdown-link-attr-modifier>=0.2.0,<0.3.0',
 'pikepdf>=5.1.1',
 'pillow',
 'psycopg2',
 'redis',
 'whitenoise>=6.0.0,<7.0.0']

extras_require = \
{':python_version >= "3.8" and python_version < "3.9"': ['backports.zoneinfo'],
 'reviewpanel': ['reviewpanel>=0.6.5,<0.7.0']}

setup_kwargs = {
    'name': 'formative',
    'version': '0.9.2',
    'description': 'Self-hosted web app for collecting form responses and files',
    'long_description': '**Formative** is a self-hosted web app for collecting form responses and\nfiles. For application forms, you can use it together with\n[reviewpanel](https://github.com/johncronan/reviewpanel) to review and score\napplicant submissions.\n\nDevelopment of Formative was funded by\n[Public Media Institute](https://publicmediainstitute.com), with support from\n[The Andy Warhol Foundation for the Visual Arts](https://warholfoundation.org).\n',
    'author': 'John Kyle Cronan',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/johncronan/formative',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
