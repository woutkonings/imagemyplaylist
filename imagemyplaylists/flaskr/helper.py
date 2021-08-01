from .config import Config


def determine_host(headers):
    dict_headers = dict(headers)
    if dict_headers['Host'] == 'spotify.pics':
        return Config.CALLBACK_URL_EXTERNAL
    else:
        return Config.CALLBACK_URL_LOCAL
