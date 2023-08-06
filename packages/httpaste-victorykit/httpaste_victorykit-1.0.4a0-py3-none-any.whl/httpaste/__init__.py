#!/usr/bin/env python3
"""PSEUDO-MAN-PAGE

NAME

    httpaste - versatile HTTP pastebin

SYNOPSIS

    HTTP [POST|PUT|DELETE|GET] {url}paste/[public|private]

    {url}ui

DESCRIPTION

    This program offers an HTTP interface for storing public and private data
    (a.k.a. pastes). Public data can be accessed through an URL, where as 
    private pastes additionally require HTTP basic authentication. Creation of
    authentication credentials happens on the fly, there is no sign-up process.
    Public pastes can only be accessed by knowing their paste ids, they are not
    listed on any index, since it isn't technically possible (by design).

    All pastes are symetrically encrypted with an HMAC derived key using 
    {hmac_iterations} iterations and SHA-512 hashing, a server-side salt and a 
    randomly generated password. Public paste's passwords are derived from 
    their ids. Private paste's passwords are randomly generated and stored 
    inside a symetrically encrypted personal database, with the encryption key 
    also being derived through the same HMAC mechanism, where the HTTP basic 
    authentication credentials act as the master password.

    Paste ids, usernames, and any other identifiable attributes are only stored
    inside databases as keyed and salted BLAKE2 hashes.

    Default Paste Encoding: {paste_default_encoding}
    Default Paste Lifetime: {paste_lifetime} minutes
    Minimum Paste Lifetime: 1 minute
    Maximum Paste Lifetime: {paste_max_lifetime} hours

EXAMPLES

    POST Public Paste

        $ echo '#My public paste' | curl {url}paste/public \\
              -F 'data=<-'
        {url}/paste/private/I0ah7fyA


    GET Public Paste

        $ curl {url}/paste/public/I0ah7fyA
        #My public paste


    POST Private Paste

        $ echo '#My private paste' | curl {url}paste/private \\
              -F 'data=<-' \\
              -u myusername:mypassword
        {url}paste/private/4FtNL75g


    GET Private Paste

        $ curl {url}paste/private -u myusername:mypassword
        #My private paste


    POST Paste (with non-default expiration)

        $ echo '#My paste expires in 20 minutes' | curl \\
              {url}paste/public?lifetime=20 \\
              -F 'data=<-' \\
        {url}paste/public/xMxEmNi8


    POST Paste (with expiration after first read)

        $ echo '#My paste expires after first read' | curl \\
              {url}paste/public?lifetime=-1 \\
              -F 'data=<-' \\
        {url}paste/public/4FtNL75g


    POST Paste with binary data

        $ cat my.pdf | base64 | curl \\
              "{url}paste/public?encoding=base64" \\
              -F "data=<-"
        {url}paste/public/zYWpEzXU


    GET Paste (with shell syntax highlighting)

        $ curl "{url}paste/public/I0ah7fyA?syntax=json"
        [38;5;66;03m#My public paste[39;00m


    GET Paste (with line numbers)

        $ curl "{url}paste/public/I0ah7fyA?syntax=shell&linenos=true"
        0001: [38;5;66;03m#My public paste[39;00m
        0002:


    GET Paste (with formatted output)

        $ curl "{url}paste/public/I0ah7fyA?syntax=shell&format=html"
        --e.g. HTML OUTPUT WITH INLINE CSS--


    GET Paste (and set HTTP response content type)

        $ curl "{url}paste/public/zYWpEzXU?mime=application/pdf"
        --e.g. BINARY--

SEE ALSO

    Documentation <https://victorykit.bitbucket.org/httpaste>

    Sources       <https://bitbucket.org/victorykit/httpaste>

    Host (HTTPS)  <https://httpaste.it>
         (HTTP)   <http://httpaste.it>

NOTES

    THIS PROGRAM IS FREE SOFTWARE.

    IN NO EVENT UNLESS REQUIRED BY APPLICABLE LAW OR AGREED TO IN WRITING
    WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MODIFIES AND/OR CONVEYS
    THE PROGRAM AS PERMITTED, BE LIABLE TO YOU FOR DAMAGES, INCLUDING ANY
    GENERAL, SPECIAL, INCIDENTAL OR CONSEQUENTIAL DAMAGES ARISING OUT OF THE
    USE OR INABILITY TO USE THE PROGRAM (INCLUDING BUT NOT LIMITED TO LOSS OF
    DATA OR DATA BEING RENDERED INACCURATE OR LOSSES SUSTAINED BY YOU OR THIRD
    PARTIES OR A FAILURE OF THE PROGRAM TO OPERATE WITH ANY OTHER PROGRAMS),
    EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF
    SUCH DAMAGES.

"""
from typing import NamedTuple, Tuple, Any
from string import ascii_uppercase, digits, ascii_letters, punctuation
from inspect import isclass
from configparser import ConfigParser
from ast import literal_eval
from io import StringIO

from connexion import FlaskApp
from connexion.resolver import RestyResolver

from httpaste.model import Backend
from httpaste.backend import get_backend_map
from httpaste.helper.common import generate_random_string
from httpaste.helper.http import (
    BadRequestError,
    ForbiddenError,
    GoneError,
    NotFoundError,
    UnauthorizedError)


CONFIGPATH_ENVIRON = 'HTTPASTE_CONFIG'


def get_sanitized_config_charset(charset: str):

    for x in ["$", "%"]:

        charset = charset.replace(x, f'{x}{x}')

    return charset


class ConfigError(Exception):
    """Config Exception
    """


class Config:
    """httpaste global config
    """
    salt: bytes = get_sanitized_config_charset(generate_random_string(
        32, ascii_letters + digits + punctuation)).encode('utf-8')
    paste_id_size: int = 8
    paste_id_charset: str = ascii_letters + digits
    paste_key_size: int = 32
    paste_key_charset: str = get_sanitized_config_charset(
        ascii_letters + digits + punctuation)
    paste_lifetime: int = 5
    backend: Backend = None
    hmac_iterations: int = 20000
    paste_default_encoding: str = 'utf-8'


class ServerConfig:
    """connexion config
    """
    swagger_ui: bool = True
    bind_address = None


def get_config_path(environ: str = CONFIGPATH_ENVIRON):
    """
    """

    try:

        return os.environ[environ]
    except KeyError as e:

        raise ConfigError(
            'environment variable \'{environ}\' not set.') from e


def load_config(path: str) -> Tuple[Config, ServerConfig]:
    """get config objects from file
    """

    _config = ConfigParser()
    _config.read(path)

    backends = get_backend_map()
    bconf = dict(_config.items('backend'))
    btype = bconf.pop('type')

    try:
        bcl, bparamcl = backends[btype]
    except KeyError as e:
        bids = ', '.join(backends.keys())
        raise ConfigError(' '.join((
            f'invalid backend \'{btype}\' in \'{path}\'. ',
            f'must be any of [{bids}]'
        ))) from e

    config = dict(_config.items('general'))
    server_config = dict(_config.items('server'))

    c = Config()
    sc = ServerConfig()

    # typecast model_backend section items
    bconf = {k: literal_eval(v) for k, v in bconf.items()}
    # initialize model backend
    c.backend = bcl(bparamcl(**bconf))

    # typecast general section items
    for k, v in config.items():
        setattr(c, k, literal_eval(v))
    # typecast server section items
    for k, v in server_config.items():
        setattr(sc, k, literal_eval(v))

    c.salt = c.salt.encode('utf-8')

    return c, sc


def default_config() -> str:
    """
    """

    config = ConfigParser()

    config['general'] = {
        'salt': Config.salt.decode('utf-8'),
        'paste_key_charset': Config.paste_key_charset,
        'paste_id_charset': Config.paste_id_charset
    }

    for literal in [
        'paste_id_size',
        'paste_key_size',
        'paste_lifetime'
    ]:
        config['general'][literal] = str(getattr(Config, literal))

    config['backend'] = {
        'type': 'sqlite',
        'path': 'file::memory:?cache=shared'
    }

    config['server'] = {}
    for literal in [
        'swagger_ui',
        'bind_address'
    ]:
        config['server'][literal] = str(getattr(ServerConfig, literal))

    stream = StringIO()
    config.write(stream)
    stream.seek(0)

    return stream.read()


def get_flask_app(
        config: Config,
        server_config: ServerConfig = ServerConfig) -> FlaskApp:
    """get a flask app object
    """

    options = {"swagger_ui": server_config.swagger_ui}

    application = FlaskApp(__name__, specification_dir='schema/')

    application.add_api(
        'httpaste.openapi.json',
        options=options,
        resolver=RestyResolver('httpaste.controller')
    )

    for err_cls in [
        BadRequestError,
        ForbiddenError,
        GoneError,
        NotFoundError,
        UnauthorizedError
    ]:
        application.add_error_handler(
            err_cls, getattr(err_cls, 'render')
        )

    with application.app.app_context():
        application.app.httpaste = config

    return application


__all__ = [
    Config,
    ServerConfig,
    load_config,
    default_config,
    get_flask_app
]
