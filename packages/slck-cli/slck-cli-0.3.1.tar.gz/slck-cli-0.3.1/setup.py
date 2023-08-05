# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slck']

package_data = \
{'': ['*']}

install_requires = \
['fire>=0.4,<0.5', 'python-dotenv>=0.19,<0.20', 'slack-sdk>=3.0,<4.0']

entry_points = \
{'console_scripts': ['slck = slck.cli:main']}

setup_kwargs = {
    'name': 'slck-cli',
    'version': '0.3.1',
    'description': 'Simple cli tool to manage your slack workspace',
    'long_description': '# slck-cli: Simple cli tool to manage your slack workspace\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/slck-cli)\n![PyPI](https://img.shields.io/pypi/v/slck-cli)\n[![GitHub license](https://img.shields.io/github/license/joe-yama/slck-cli)](https://github.com/joe-yama/slck-cli/blob/main/LICENSE)\n[![codecov](https://codecov.io/gh/joe-yama/slck-cli/branch/main/graph/badge.svg?token=H4VWW055ER)](https://codecov.io/gh/joe-yama/slck-cli)\n[![Run tests](https://github.com/joe-yama/slck-cli/actions/workflows/run-tests.yml/badge.svg?branch=main)](https://github.com/joe-yama/slck-cli/actions/workflows/run-tests.yml)\n\n## Basic Usage\n\n```bash\n# listing all users in workspace\n$ slck user list\nUser(id=\'U031L3JNBKS\', name=\'taro\', real_name=\'Taro Yamada\')\nUser(id=\'U036NS9S6HL\', name=\'jiro\', real_name=\'Jiro Tanaka\')\nUser(id=\'U032SU3SKBS\', name=\'hanako\', real_name=\'Hanako Suzuki\')\n\n# user search by real_name (or name or id)\n$ slck user find --real_name "Taro Yamada"\nUser(id=\'U031L3JNBKS\', name=\'taro\', real_name=\'Taro Yamada\')\n\n# channel list (filtered by prefix)\n$ slck channel list --prefix general\nChannel(id=\'C02AFAUOK33\', name=\'general\')\n\n# most reacted post in the channel\n$ slck message popular general\nMessage(message_type=\'message\', user=User(id=\'U031L3JNBKS\', name=\'taro\', real_name=\'Taro Yamada\'), channel=Channel(id=\'C02AFAUOK33\', name=\'general\'), ts=\'1647648476.156199\', text=\'テスト\', num_reply=0, num_replyuser=0, num_reaction=3, permalink=\'https://foo.slack.com/archives/C02AFAUOK33/p23471289471123\')\n\n# post award message\n$ slck message award your-channel --post\nBot is about to post award message:\n  最もリアクションを獲得したのは <@U031L3JNBKS|taro>さんのこのポスト！おめでとうございます！:raised_hands:\nhttps://foo.slack.com/archives/C02AFAUOK33/\nto your-channel. Are you sure? [Y/n]Y\nPosted!\n```\n\n## Installation\n\n```bash\npip install slck-cli\n```\n\n## Preparation\n\n### Create SlackApp and Install to your workspace\n\n- [Create a new Slack app](https://api.slack.com/authentication/basics#creating)\n- [Add scopes to your Bot Token](https://api.slack.com/authentication/basics#scopes)  \nIn order to use all the feature of `slck-cli` , add scopes bellow:\n  - `channels:history`\n  - `channels:join`\n  - `channels:manage`\n  - `channels:read`\n  - `groups:history`\n  - `groups:read`\n  - `groups:write`\n  - `im:history`\n  - `im:read`\n  - `im:write`\n  - `mpim:history`\n  - `mpim:read`\n  - `mpim:write`\n  - `users:read`\n  - `chat:write`\n- [Install app to your workspace](https://api.slack.com/authentication/basics#installing)\n\n### Set token\n\nSet your slack bot token ( `xoxb-...` ) to your environmental varialble `SLACK_BOT_TOKEN`\n\n```bash\nexport SLACK_BOT_TOKEN = "xoxb-your-token"\n```\n\n## License\n\nThis software is released under the MIT License, see LICENSE.\n',
    'author': 'joe-yama',
    'author_email': 's1r0mqme@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/joe-yama/slck-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.10',
}


setup(**setup_kwargs)
