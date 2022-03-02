# Config

Ghost Detector can be configured with a JSON file at `ghost_detector/config.json`.
[ghost_detector/config_example.json](../ghost_detector/config_example.json) contains
default values and can be used as a template. `bot_token` is the only required
field.

## Config Fields

### (root)

Fields in the root JSON object.

| Key                    | Value                                                                                     |
|------------------------|-------------------------------------------------------------------------------------------|
| `bot_token` *(string)* | Your [Discord bot's](https://discord.com/developers/docs/topics/oauth2#bots) access token |
