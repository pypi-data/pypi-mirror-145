import typer
import json
from .twitchbot import FutureToneIntegrationBot

app = typer.Typer()


def get_settings(file_path: str = 'settings.json') -> dict:
    try:
        with open(file_path, 'r') as file:
            _json = file.read()
            _settings = json.loads(_json)
        return _settings
    except FileNotFoundError:
        return {}


def set_settings(**kwargs):
    file_path = kwargs.pop('file_path', 'settings.json')
    with open(file_path, 'w') as file:
        _json = json.dumps(kwargs)
        file.write(_json)


@app.command()
def start():
    settings = get_settings()
    if settings == {}:
        settings = setup()

    with FutureToneIntegrationBot(**settings) as bot:
        bot.run()


@app.command()
def set_setting(
        ip: str = None,
        bot_token: str = None,
        access_token: str = None,
        channel: str = None,
        title_id: str = None):
    """Change bot settings."""

    changes = {
        'ps4_ip': ip,
        'bot_token': bot_token,
        'access_token': access_token,
        'twitch_channel': channel.lower(),
        'title_id': title_id,
    }
    changes = {k: v for k, v in changes.items() if v is not None}

    current_settings = get_settings()
    current_settings.update(changes)
    set_settings(**current_settings)
    return current_settings


@app.command()
def setup():
    """Setup the bot interactively"""
    ip = typer.prompt('PS4 IP (Leave empty to let the bot search for the system)', show_default=False, default='')
    access_token = typer.prompt('User access token')
    bot_token = typer.prompt('Bot access token (Leave empty to use user token)', show_default=False, default='')
    channel = typer.prompt('Twitch channel name')
    return set_setting(ip, bot_token, access_token, channel, 'CUSA06211')


if __name__ == '__main__':
    app()
