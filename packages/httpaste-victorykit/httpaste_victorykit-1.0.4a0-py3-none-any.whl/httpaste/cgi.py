#!/usr/bin/env python3
"""httpaste CGI entrypoint
"""
from wsgiref.handlers import CGIHandler
from httpaste import load_config, get_flask_app, get_config_path

config, server_config = load_config(get_config_path())

application = get_flask_app(config, server_config)

CGIHandler().run(application)
