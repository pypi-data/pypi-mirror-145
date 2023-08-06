# tasks - top-level fabric tasks: from clldappconfig.tasks import *

"""
fabric tasks
------------

We use the following mechanism to provide common task implementations for all clld apps:
This module defines and exports tasks which take a first argument "environment".
The environment is used to determine the correct host to run the actual task on.
To connect tasks to a certain app, the app's fabfile needs to import this module
and run the init function, passing an app name defined in the global clld app config.
"""

import os
import pathlib

import functools
import fabric.api

import clldappconfig as appconfig
from .. import helpers

__all__ = ["init", "task_app_from_environment"]

APP = None


fabric.api.env.use_ssh_config = True  # configure your username in .ssh/config


def init(app_name=None):
    """initialize appconfig configuration.  Expects the following folder structure:

    /.../apps.ini
    /.../myapp/fabfile.py

    so the parent of the apps fabfile directory has to contain the apps.ini.

    Alternatively the environment varialbel APPCONFIG_DIR can be set with a path
    to the directory containing the apps.ini file.
    """
    global APP

    if os.environ.get("APPCONFIG_DIR"):
        appconfig.init(os.environ.get("APPCONFIG_DIR"))
    else:
        appconfig.init(pathlib.Path(helpers.caller_dir()).parent)

    if app_name is None:  # pragma: no cover
        app_name = helpers.caller_dirname()
    APP = appconfig.APPS[app_name]


def task_app_from_environment(func_or_environment):
    if callable(func_or_environment):
        func, _environment = func_or_environment, None
    else:
        func, _environment = None, func_or_environment

    if func is not None:

        @functools.wraps(func)
        def wrapper(environment, *args, **kwargs):
            assert environment in ("production", "test", "staging")
            if not fabric.api.env.hosts:
                if environment == "staging":
                    raise ValueError("staging tasks require an explicit host via -H")
                # allow overriding the hosts by using fab's -H option
                fabric.api.env.hosts = [getattr(APP, environment)]
            fabric.api.env.environment = environment
            return fabric.api.execute(func, APP, *args, **kwargs)

        wrapper.execute_inner = func
        return fabric.api.task(wrapper)
    else:

        def decorator(_func):
            _wrapper = task_app_from_environment(_func).wrapped
            wrapper = functools.wraps(_wrapper)(
                functools.partial(_wrapper, _environment)
            )
            wrapper.execute_inner = _wrapper.execute_inner
            return fabric.api.task(wrapper)

        return decorator


from .deployment import *  # noqa: F403, E402
from .other import *  # noqa: F403, E402

__all__ += deployment.__all__ + other.__all__  # noqa: F405
