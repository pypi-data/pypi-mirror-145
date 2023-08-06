from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.db.models import Model
from django.conf import settings
from django.apps import apps
from inspect import isclass
from click import echo
from importlib import import_module
import os
from firebrick.management.commands._default_ignore import default_ignore_apps


class Command(BaseCommand):
    help = 'Dumps all models data (except for User model).'
    
    def handle(self, *args, **options):
        for app in apps.app_configs:
            if app not in default_ignore_apps:
                try:
                    app_models = import_module(f'{app}.models')
                    models = True
                except ImportError:
                    models = False
                if models:
                    app_fixture_path = os.path.join(settings.BASE_DIR, app, 'fixtures', app)
                    if not os.path.isdir(app_fixture_path):
                        if not os.path.isdir(os.path.join(settings.BASE_DIR, app, 'fixtures')):
                            os.mkdir(os.path.join(settings.BASE_DIR, app, 'fixtures'))
                        os.mkdir(app_fixture_path)
                    for var in app_models.__dict__:
                        if isclass(app_models.__dict__[var]) and issubclass(app_models.__dict__[var], Model):
                            if app == app_models.__dict__[var].__repr__(app_models.__dict__[var]).split("'")[1].split('.')[0]:
                                if len(app_models.__dict__[var].objects.all()) > 0:
                                    call_command('dumpdata', f'{app}.{var}', output=os.path.join(app_fixture_path, var.lower() + ".json"), indent=4)
            