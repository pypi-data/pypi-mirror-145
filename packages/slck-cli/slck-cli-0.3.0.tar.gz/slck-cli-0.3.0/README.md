# slck-cli: Simple cli tool to manage your slack workspace

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/slck-cli)
![PyPI](https://img.shields.io/pypi/v/slck-cli)
[![GitHub license](https://img.shields.io/github/license/joe-yama/slck-cli)](https://github.com/joe-yama/slck-cli/blob/main/LICENSE)
[![codecov](https://codecov.io/gh/joe-yama/slck-cli/branch/main/graph/badge.svg?token=H4VWW055ER)](https://codecov.io/gh/joe-yama/slck-cli)
[![Run tests](https://github.com/joe-yama/slck-cli/actions/workflows/run-tests.yml/badge.svg?branch=main)](https://github.com/joe-yama/slck-cli/actions/workflows/run-tests.yml)

## Basic Usage

```bash
# listing all users in workspace
$ slck user list
User(id='U031L3JNBKS', name='taro', real_name='Taro Yamada')
User(id='U036NS9S6HL', name='jiro', real_name='Jiro Tanaka')
User(id='U032SU3SKBS', name='hanako', real_name='Hanako Suzuki')

# user search by real_name (or name or id)
$ slck user find --real_name "Taro Yamada"
User(id='U031L3JNBKS', name='taro', real_name='Taro Yamada')

# channel list (filtered by prefix)
$ slck channel list --prefix general
Channel(id='C02AFAUOK33', name='general')

# most reacted post in the channel
$ slck message popular general
Message(message_type='message', user=User(id='U031L3JNBKS', name='taro', real_name='Taro Yamada'), channel=Channel(id='C02AFAUOK33', name='general'), ts='1647648476.156199', text='テスト', num_reply=0, num_replyuser=0, num_reaction=3, permalink='https://foo.slack.com/archives/C02AFAUOK33/p23471289471123')

# post award message
$ slck message award your-channel --post
Bot is about to post award message:
  最もリアクションを獲得したのは <@U031L3JNBKS|taro>さんのこのポスト！おめでとうございます！:raised_hands:
https://foo.slack.com/archives/C02AFAUOK33/
to tmc-zatsudan. Are you sure? [Y/n]Y
Posted!
```

## Installation

```bash
pip install slck-cli
```

## Preparation

### Create SlackApp and Install to your workspace

- [Create a new Slack app](https://api.slack.com/authentication/basics#creating)
- [Add scopes to your Bot Token](https://api.slack.com/authentication/basics#scopes)  
In order to use all the feature of `slck-cli` , add scopes bellow:
  - `channels:history`
  - `channels:join`
  - `channels:manage`
  - `channels:read`
  - `groups:history`
  - `groups:read`
  - `groups:write`
  - `im:history`
  - `im:read`
  - `im:write`
  - `mpim:history`
  - `mpim:read`
  - `mpim:write`
  - `users:read`
  - `chat:write`
- [Install app to your workspace](https://api.slack.com/authentication/basics#installing)

### Set token

Set your slack bot token ( `xoxb-...` ) to your environmental varialble `SLACK_BOT_TOKEN`

```bash
export SLACK_BOT_TOKEN = "xoxb-your-token"
```

## License

This software is released under the MIT License, see LICENSE.
