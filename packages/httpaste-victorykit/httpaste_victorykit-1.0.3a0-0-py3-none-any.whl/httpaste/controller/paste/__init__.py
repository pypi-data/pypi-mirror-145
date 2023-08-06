from connexion import request
from connexion.lifecycle import ConnexionResponse
from flask import current_app

from httpaste.helper.common import decode, DecodeError, join_url
import httpaste.model.paste as paste_model
import httpaste.model.user as user_model
from httpaste.helper.http import BadRequestError, GoneError, NotFoundError
from httpaste.model import (
    PasteKey,
    PasteData,
    PasteLifetime,
    PasteEncoding,
    MasterKey,
    Sub)


def delete(**kwargs):
    """
    """

    pid = httpaste.model.PasteKey(request['id'].encode('utf-8'))
    key = httpaste.model.MasterKey(request['token_info'].get('master_key'))
    sub = httpaste.model.Sub(request['token_info'].get('sub'))

    pkey = httpaste.model.user.load_paste_key(
        pid,
        sub,
        key,
        current_app.httpaste.backend.user,
        current_app.httpaste.salt)

    httpaste.model.paste.remove_safe(
        pid,
        sub,
        pkey,
        current_app.httpaste.backend.paste,
        current_app.httpaste.salt)

    return None, 200


def get(**kwargs):
    """
    """

    config = current_app.httpaste

    pid = PasteKey(kwargs['id'].encode('utf-8'))
    syntax = kwargs.get('syntax')
    formatter = kwargs.get('format', 'terminal256')
    linenos = kwargs.get('linenos', False)
    mime = kwargs.get('mime', 'text/plain')

    if kwargs.get('user') is not None:
        # authenticated

        key = MasterKey(kwargs['token_info'].get('master_key'))
        sub = Sub(kwargs['token_info'].get('sub'))

        pkey = user_model.load_paste_key(pid, sub, key, config.backend.user,
                                         config.salt, config.hmac_iterations)

        def call(): return paste_model.get_safe(pid, pkey, sub,
                                                config.backend.paste,
                                                config.salt, config.hmac_iterations)
    else:
        # unauthenticated

        def call(): return paste_model.get(pid, config.backend.paste,
                                           config.salt, config.hmac_iterations)

    try:
        data, expiration, encoding = call()
    except paste_model.LifetimeError as e:
        if kwargs.get('user') is not None:
            paste_model.remove_safe(pid, sub, pkey, config.backend.paste, 
                                    config.salt, config.hmac_iterations)
        else:
            paste_model.remove(pid, config.backend.paste)
        raise GoneError(str(e)) from e
    except paste_model.NotFoundError as e:
        raise NotFoundError(str(e))
    except paste_model.SubError as e:
        raise ForbiddenError(str(e))

    # burn after read
    if expiration < 0:
        if kwargs.get('user') is not None:
            paste_model.remove_safe(pid, sub, pkey, config.backend.paste, 
                                    config.salt, config.hmac_iterations)
        else:
            paste_model.remove(pid, config.backend.paste)

    if syntax is not None:
        data = highlight(data, str(syntax), formatter, linenos)

    if encoding is not None:
        data = data.decode(encoding)

    return ConnexionResponse(
        status_code=200,
        content_type=mime,
        body=data
    )


def post(**kwargs):
    """
    """

    config = current_app.httpaste

    if kwargs['body'].get('data') is None:
        raise BadRequestError('form field \'data\' missing.')

    encoding = PasteEncoding(kwargs.get('encoding', 'utf-8'))
    lifetime = PasteLifetime(kwargs.get('lifetime', config.paste_lifetime))

    if encoding not in ['utf-8', 'utf-16', 'ascii']:
        try:
            decoded_data = decode(kwargs['body'].get('data'), encoding)
        except DecodeError as e:
            raise BadRequestError(str(e))
        else:
            pdata = PasteData(decoded_data)
        encoding = None
    else:
        pdata = PasteData(kwargs['body']['data'].encode(encoding))

    if kwargs.get('user') is not None:
        # authenticated

        key = MasterKey(kwargs['token_info'].get('master_key'))
        sub = Sub(kwargs['token_info'].get('sub'))

        pid, pkey = paste_model.create_safe(pdata, lifetime, sub, encoding,
                                            config.backend.paste, config.salt, config.hmac_iterations)

        user_model.dump_paste_key(pid, pkey, sub, key, config.backend.user,
                                  config.salt, config.hmac_iterations)
    else:
        # unauthenticated

        pid = paste_model.create(pdata, lifetime, encoding, config.backend.paste,
                                 config.salt, config.hmac_iterations)


    base_url = join_url(request.root_url, request.path)

    url = '/'.join((base_url, pid.decode('utf-8')))

    return '\n'.join((url, '')), 200
