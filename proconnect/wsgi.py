"""
WSGI config for proconnect project.
"""

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proconnect.settings')

# Auto-run migrations on Vercel (fresh /tmp SQLite on every cold start)
if os.environ.get('VERCEL'):
    from django.core.management import call_command
    try:
        call_command('migrate', '--run-syncdb', verbosity=0)
    except Exception:
        pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

