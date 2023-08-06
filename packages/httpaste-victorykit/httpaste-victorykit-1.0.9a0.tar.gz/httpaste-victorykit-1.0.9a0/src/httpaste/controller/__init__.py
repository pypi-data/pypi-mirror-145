import connexion
from flask import current_app
import httpaste

def get(**kwargs):

    config = current_app.httpaste


    return httpaste.__doc__.format(
        url=connexion.request.url,
        hmac_iterations=config.hmac_iterations,
        paste_lifetime=config.paste_lifetime,
        paste_max_lifetime=str(round(config.paste_max_lifetime / 60)),
        paste_default_encoding=config.paste_default_encoding
    ), 200
