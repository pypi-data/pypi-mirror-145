# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wheat',
 'wheat.calendar',
 'wheat.console',
 'wheat.console.commands',
 'wheat.console.commands.task',
 'wheat.harvest',
 'wheat.harvest.projects',
 'wheat.utils']

package_data = \
{'': ['*'], 'wheat.calendar': ['client_credentials/*']}

install_requires = \
['cleo==1.0.0a4',
 'google-api-python-client>=2.42.0,<3.0.0',
 'google-auth-httplib2>=0.1.0,<0.2.0',
 'google-auth-oauthlib>=0.5.1,<0.6.0',
 'pendulum>=2.1.2,<3.0.0',
 'tomlkit>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['wheat = wheat.console.application:main']}

setup_kwargs = {
    'name': 'wheat',
    'version': '0.8.0',
    'description': 'A concise and fast CLI to log hours in Harvest.',
    'long_description': '# Wheat #\n\nA concise and fast CLI to log hours in Harvest.\n\n## Managing Projects ##\n\nWheat keeps a "projects" file somewhere that it stores task information in. Users can set tasks as active/not active at will. Whatever tasks are present in the task file are shown each time the user is asked to do anything regarding tasks.\n\n## Commands ##\n\nauth: Authenticate with Harvest by providing a personal access token and account id.\n\ntask:\n    list: Displays your Current Projects and Tasks.\n    activate: Set a Project or Task as active.\n    sleep: Set a Project or Task as inactive.\n\nmeetings:\n    next: Displays your next meeting.\n    today: Displays today\'s meetings.\n    join: Joins a meeting\'s video chat if a link is provided.\n        Supports <c1>Zoom</c1> and <c1>Google Meets</c1>.\n            * Takes Meeting ID as an argument. If none is provided, joins the next meeting on the calendar, if it can.\n\nNote: Meetings commands require you to have logged into your Google account, and will use events from your google calendar.\n',
    'author': 'etschz',
    'author_email': 'ethanschmitz214@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etschz/wheat',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
