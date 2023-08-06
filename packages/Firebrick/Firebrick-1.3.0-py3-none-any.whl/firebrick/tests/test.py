from django.urls import resolve, reverse
from django.test import Client
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth.models import User


def get_reverse_url(instance):
    if '/' not in instance.name:
        if 'args'in dir(instance):
           return reverse(instance.name, args=instance.args)
        elif 'arg_success' in dir(instance):
            return reverse(instance.name, args=instance.arg_success)
        return reverse(instance.name)
    else:
        return instance.name


class ResolveUrlTest:
    def test_url_is_resolved(self):
        url = get_reverse_url(self)
        
        if '__func__' in dir(self.view):
            self.assertEquals(resolve(url).func, self.view.__func__)
        else:
            self.assertEquals(resolve(url).func.view_class, self.view)


class GetViewTest:
    def test_GET(self):
        client = Client()
        
        url = get_reverse_url(self)
        
        response = client.get(url)
        
        self.assertEquals(response.status_code, self.status)
        self.assertTemplateUsed(response, self.template)


class GetViewOr404Test:
    def test_GET_success(self):
        client = Client()
        
        call_command('loaddata', *self.fixtures, verbosity=0)
        
        url = reverse(self.name, args=self.arg_success)
        
        response = client.get(url)
        
        self.assertEquals(response.status_code, self.status_success)
        self.assertTemplateUsed(response, self.template_success)
        
    def test_GET_404(self):
        client = Client()
        
        call_command('loaddata', *self.fixtures, verbosity=0)
        
        url = reverse(self.name, args=self.arg_fail)
        
        response = client.get(url)
        
        self.assertEquals(response.status_code, self.status_fail)
        self.assertTemplateNotUsed(response, self.template_success)
        
        if 'template_fail' in dir(self):
            self.assertTemplateUsed(response, self.template_fail)
            
            
class GetLoginRequired:
    def test_GET_not_logged_in(self):
        client = Client()
        
        url = get_reverse_url(self)
        
        response = client.get(url)
        
        self.assertRedirects(response, f'{reverse(settings.LOGIN_URL)}?next={url}')
        
    def test_GET_logged_in(self):
        User.objects.create_user(username='testuser1', password='thisisapassword')
        
        client = Client()
        
        url = get_reverse_url(self)
        
        client.login(username='testuser1', password='thisisapassword')
        response = client.get(url)
        
        self.assertEquals(response.status_code, self.status)
        self.assertTemplateUsed(response, self.template)
    