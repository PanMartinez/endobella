# pyright: reportMissingTypeStubs=true
from __future__ import annotations


import environ
from django.core.exceptions import ImproperlyConfigured


class Env(environ.Env):
    def __init__(self, ignore_required=False, **scheme):
        self.ignore_required = ignore_required
        super().__init__(**scheme)

    def get_value(
        self, var, cast=None, default=environ.Env.NOTSET, parse_default=False
    ):
        try:
            return super().get_value(var, cast, default, parse_default)
        except ImproperlyConfigured as e:
            if self.ignore_required:
                if not cast:
                    return None
                return cast("")
            raise e


env = Env()
