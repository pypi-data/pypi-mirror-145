from django.core.exceptions import BadRequest
import json


class Serializer:
    @classmethod
    def data(cls, request):
        '''
        Turns json to model object
        '''

        try:
            body = json.loads(request.body)
        except:
            raise BadRequest('Body is not valid json data.')

        fields_data = {}

        for field in cls.Meta.fields:
            try:
                fields_data[field] = body[field]
            except KeyError:
                raise BadRequest(f'{field} is required.')
        
        return cls.Meta.model.objects.get_object_or_404(**fields_data, error_text='Object could not be found.')

    @classmethod
    def parse(cls, model_object):
        '''
        Turns model object to json
        '''
        
        pass
