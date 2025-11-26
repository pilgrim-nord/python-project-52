#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


if os.path.exists('/project/.venv'):
    activate_this = '/project/.venv/bin/activate_this.py'
    if os.path.exists(activate_this):
        exec(open(activate_this).read(), {'__file__': activate_this})
else:
    # Fallback: добавляем стандартный site-packages (для Python 3.13/3.12)
    site_packages = '/project/.venv/lib/python3.13/site-packages'  # Измени на 3.12, если нужно
    if os.path.exists(site_packages):
        sys.path.insert(0, site_packages)

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_manager.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
