#!/usr/bin/env python
import os
import sys

# Other than the wsgi.py file, this manage.py file always uses the `local`
# settings, since it is only ran on dev machines.
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hub.settings.local")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
