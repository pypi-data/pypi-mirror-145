from django.core.exceptions import BadRequest
import json


class Argument:
    def __init__(self, name, type, required, help_msg):
        self.name = name
        self.type = type
        self.required = required
        self.help_msg = help_msg


class RequestParser:
    def __init__(self):
        self.argument_list = []

    def add_argument(self, name, type=None, required=False, help_msg='Missing argument'):
        self.argument_list.append(Argument(name, type, required, help_msg))

    def parse(self, request):
        data = {}

        try:
            body = json.loads(request.body)
        except:
            raise BadRequest('Body is not valid json.')

        for arg in self.argument_list:
            try:
                value = body[arg.name]
                if arg.type:
                    if type(value) != arg.type:
                        value = arg.type(value)
                data[arg.name] = value
            except KeyError:
                if arg.required:
                    raise BadRequest(arg.help_msg)

        return body