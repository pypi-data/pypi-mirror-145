from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from django.apps import apps
from click import echo
import os
from firebrick.management.commands._default_ignore import default_ignore_apps


class Command(BaseCommand):
    help = 'Loads all fixtures.'
    
    def handle(self, *args, **options):
        for app in apps.app_configs:
            if app not in default_ignore_apps:
                app_fixture_path = os.path.join(settings.BASE_DIR, app, 'fixtures', app)
                if os.path.isdir(app_fixture_path):
                    fixtures = [f for f in os.listdir(app_fixture_path) if os.path.isfile(os.path.join(app_fixture_path, f)) and f.endswith('.json') or f.endswith('.yaml')]
                    for fixture in fixtures:
                        call_command('loaddata', os.path.join(app_fixture_path, fixture), verbosity=0)