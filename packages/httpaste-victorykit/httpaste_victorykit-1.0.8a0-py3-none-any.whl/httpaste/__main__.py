"""Main
"""
import argparse
import os
from importlib.resources import open_text


def _this_dir(basename: str) -> str:
    """build path with script directory name and provided basename
    """

    return os.path.join(os.path.dirname(__file__), basename)


def _path_output(path, echo: bool = False) -> str:
    """print path content or path
    """

    if not echo:

        return path
    else:

        with open_text('httpaste', path) as fh:

            return fh.read()


def command_standalone(**kwargs):
    """run standalone evaluation server
    """

    from httpaste import load_config, get_flask_app

    try:
        from gevent.pywsgi import WSGIServer
    except ImportError as e:
        raise ImportError(' '.join((
            'gevent is currently not installed.',
            'Please install it by running \'python3 -m pip install gevent\'.'
        ))) from e

    config, server_config = load_config(kwargs.get('config_path'))

    application = get_flask_app(config, server_config)

    http_server = WSGIServer(('', kwargs.get('port')), application)
    http_server.serve_forever()


def command_wsgi(**kwargs):
    """get WSGI script
    """

    print(_path_output('wsgi.py', kwargs.get('echo')))


def command_cgi(**kwargs):
    """get CGI script
    """

    print(_path_output('cgi.py', kwargs.get('echo')))


def command_fcgi(**kwargs):
    """get FastCGI script
    """

    print(_path_output('fcgi.py', kwargs.get('echo')))


def command_default_config(**kwargs):
    """get default config
    """

    from httpaste import default_config

    dconfig = default_config()

    if kwargs.get('config'):

        with open(kwargs.get('config'), 'w') as fh:

            fh.write(dconfig)

            return

    print(dconfig)


def command_init_backend(**kwargs):
    """initialize the backend
    """

    from httpaste import load_config

    config, _ = load_config(kwargs.get('config'))

    config.backend.user.init()
    config.backend.paste.init()


def command_sanitize_backend(**kwargs):
    """sanitize the backend
    """

    from httpaste import load_config

    config, _ = load_config(kwargs.get('config'))

    config, _ = load_config(kwargs.get('config'))

    config.backend.user.sanitize()
    config.backend.paste.sanitize()


def parser():

    p = argparse.ArgumentParser(description='Process some integers.')

    sp = p.add_subparsers(dest='command', required=True)

    p_standalone = sp.add_parser('standalone', help=command_standalone.__doc__)
    p_standalone.add_argument('--config-path', '-c', required=True)
    p_standalone.add_argument('--port', '-p', default=8080)

    p_wsgi = sp.add_parser('wsgi', help=command_wsgi.__doc__)
    p_wsgi.add_argument('--echo', '-e', action='store_true')

    p_cgi = sp.add_parser('cgi', help=command_cgi.__doc__)
    p_cgi.add_argument('--echo', '-e', action='store_true')

    p_fcgi = sp.add_parser('fcgi', help=command_fcgi.__doc__)
    p_fcgi.add_argument('--echo', '-e', action='store_true')

    p_default_config = sp.add_parser(
        'default-config',
        help=command_default_config.__doc__)
    p_default_config.add_argument('--dump', '-d')

    p_init_backend = sp.add_parser(
        'init-backend',
        help=command_init_backend.__doc__)
    p_init_backend.add_argument('--config', '-c', required=True)

    p_sanitize_backend = sp.add_parser(
        'sanitize-backend',
        help=command_sanitize_backend.__doc__)
    p_sanitize_backend.add_argument('--config', '-c', required=True)

    return p


def main():

    p = parser()

    kwargs = vars(p.parse_args())

    {
        'standalone': command_standalone,
        'wsgi': command_wsgi,
        'cgi': command_cgi,
        'fcgi': command_fcgi,
        'default-config': command_default_config,
        'init-backend': command_init_backend,
        'sanitize-backend': command_sanitize_backend
    }[kwargs.pop('command')](**kwargs)


if __name__ == '__main__':

    main()
