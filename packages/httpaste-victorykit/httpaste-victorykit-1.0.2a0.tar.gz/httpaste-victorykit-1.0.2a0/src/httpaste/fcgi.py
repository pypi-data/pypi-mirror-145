#!/usr/bin/env python3
"""httpaste FastCGI entrypoint
"""
from flup.server.fcgi import WSGIServer
from httpaste import load_config, get_flask_app, get_config_path

config, server_config = load_config(get_config_path())

application = get_flask_app(config, server_config)

if __name__ == '__main__':

    WSGIServer(application, bindAddress=server_config.bind_address).run()
