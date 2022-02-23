import logging

logging.basicConfig(level=logging.INFO, file='sample.log')
from user.models import  LogTable


class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("Welcome to FundoNotes Application")

        response = self.get_response(request)
        log = LogTable(type_of_request=request.method, response=response.data['message'])
        log.save()

        return response
