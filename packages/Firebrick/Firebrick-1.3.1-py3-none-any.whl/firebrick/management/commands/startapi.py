from django.core.management.base import BaseCommand, CommandError
from firebrick.templates.templating import GenerateFromTemplate, TemplateFromFiles
from click import echo
import os


class Command(BaseCommand):
    help = 'Creates a firebrick api app.'

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)
    
    def handle(self, name, *args, **options):
        if not os.path.isdir(os.path.join(os.getcwd(), 'api')):
            os.mkdir(os.path.join(os.getcwd(), 'api'))
            with open(os.path.join(os.getcwd(), 'api', '__init__.py'), 'w') as f:
                pass
        
        GenerateFromTemplate(
            [
                TemplateFromFiles('api', base_local_path=os.path.join('api', name))
            ],
            context={
                '{{appconfig-name}}': name.capitalize(),
                '{{name}}': name
            }
        )