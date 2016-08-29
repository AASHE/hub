#!/usr/bin/env python
import os
import sys

# Other than the wsgi.py file, this manage.py file always uses the `local`
# settings, since it is only ran on dev machines.
if __name__ == "__main__":
    # Use the local settings file if one is present, otherwise the server.
    try:  # Use local settings if available.
        import hub.settings.local
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "hub.settings.local")
    except ImportError:  # Else, use dev_server settings if available.
        import hub.settings.dev_server  # NOQA
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "hub.settings.dev_server")
    except ImportError:  # Else, use server settings.
        os.environ.setdefault("DJANGO_SETTINGS_MODULE",
                              "hub.settings.server")

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
