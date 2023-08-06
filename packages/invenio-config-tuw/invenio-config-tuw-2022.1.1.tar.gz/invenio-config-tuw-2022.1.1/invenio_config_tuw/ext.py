# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 - 2021 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Invenio module containing some customizations and configuration for TU Wien."""

from flask_security.signals import user_registered

from . import config
from .auth.utils import auto_trust_user
from .permissions import TUWRecordPermissionPolicy


@user_registered.connect
def auto_trust_new_user(sender, user, **kwargs):
    # NOTE: 'sender' and 'kwargs' are ignored, but they're required to match the
    #       expected function signature
    # NOTE: this function won't be called when a user is created via the CLI
    #       ('invenio users create'), because it doesn't send the 'user_registered'
    #       signal
    auto_trust_user(user)


class InvenioConfigTUW(object):
    """Invenio-Config-TUW extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-config-tuw"] = self

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        for k in dir(config):
            if len(k.replace("_", "")) >= 3 and k.isupper():
                app.config.setdefault(k, getattr(config, k))

        # the datacenter symbol seems to be the username for DataCite Fabrica
        key = "DATACITE_DATACENTER_SYMBOL"
        if not app.config.get(key, None):
            app.config[key] = app.config["DATACITE_USERNAME"]
