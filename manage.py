#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pirmasProjektas.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()


# # get the directory of the current Python script file
# SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
#
# # path to your Django project's manage.py file
# MANAGE_PY_PATH = os.path.join(SCRIPT_DIR, 'manage.py')
#
# # command to run the Django development server
# COMMAND = f'python {MANAGE_PY_PATH} runserver'
#
# # path to the Microsoft Edge executable file
# EDGE_PATH = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
#
# # open the application URL in Microsoft Edge
# subprocess.run([EDGE_PATH, 'http://127.0.0.1:8000/'])

# open a new terminal window and run the command
# subprocess.call(['cmd.exe', '/k', COMMAND])
