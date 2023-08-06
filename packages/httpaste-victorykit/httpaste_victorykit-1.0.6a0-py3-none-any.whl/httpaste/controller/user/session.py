"""
"""
from flask import current_app

from httpaste.helper.http import ForbiddenError
from httpaste.model.user import authenticate, AuthenticationError


def post(*args, **kwargs):
    """
    """

    config = current_app.httpaste

    user_id = args[0].encode('utf-8')
    password = args[1].encode('utf-8')

    try:

        return authenticate(user_id, password, config.backend.user, config.salt, config.hmac_iterations)
    except AuthenticationError as e:

        raise ForbiddenError('You shall not pass!') from e
