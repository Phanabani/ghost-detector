# Ghost Detector

[![release](https://img.shields.io/github/v/release/phanabani/ghost-detector)](https://github.com/phanabani/ghost-detector/releases)
[![license](https://img.shields.io/github/license/phanabani/ghost-detector)](LICENSE)

A Discord bot that will help you find inactive users in your server.

## Table of Contents

- [Install](#install)
- [Usage](#usage)
- [Config](#config)
- [Developers](#developers)
- [License](#license)

## Install

### Prerequisites

- [Poetry](https://python-poetry.org/docs/#installation) – dependency manager
- (Optional) pyenv – Python version manager
    - [pyenv](https://github.com/pyenv/pyenv) (Linux, Mac)
    - [pyenv-win](https://github.com/pyenv-win/pyenv-win) (Windows)
- (Optional) [PM2](https://pm2.keymetrics.io/docs/usage/quick-start) – process manager

### Install Ghost Detector

To get started, clone the repo.

```shell
git clone https://github.com/phanabani/ghost-detector.git
cd ghost-detector
```

Install the dependencies with Poetry. Ghost Detector requires Python 3.9.6+.

```shell
poetry install --no-root --no-dev
```

## Usage

### Set up configuration

Create a json file `ghost_detector/config.json` (or copy [ghost_detector/config_example.json](ghost_detector/config_example.json)).
The only value you need to set is the `bot_token`.

```json
{
    "bot_token": "YOUR_BOT_TOKEN"
}
```

See [config](#config) for more info.

### Running Ghost Detector

#### Basic

In the top level directory, simply run Ghost Detector as a Python module with Poetry.

```shell script
poetry run python -m ghost_detector
```

#### With PM2

You can run the bot as a background process using PM2. Ensure you've followed
the virtual environment setup described above, then simply run the following
command in Ghost Detector's root directory:

```shell script
pm2 start
```

This starts the process as a daemon using info from [ecosystem.config.js](ecosystem.config.js).

### Inviting Ghost Detector to your Discord server

Ghost Detector requires the following permissions to run normally:

- Send messages
- Send messages in threads
- View Channels
- Embed links
- Attach files
- Read message history

## Config

Ghost Detector can be configured with a JSON file at `ghost_detector/config.json`.
[ghost_detector/config_example.json](ghost_detector/config_example.json) contains
default values and can be used as a template. `bot_token` is the only required
field.

See [Config](docs/config.md) for detailed information about setting up the
config file.

## Developers

### Installation

Follow the installation steps in [install](#install) and use Poetry to 
install the development dependencies:

```bash
poetry install --no-root
```

## License

[MIT © Phanabani.](LICENSE)
