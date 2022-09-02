from http.client import INTERNAL_SERVER_ERROR
from django.http import HttpResponse
import json
import traceback


class CustomViewExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

    def process_exception(self, request, exception):
        response_data = {}
        headers = {"Content-Type": "application/json"}
        if hasattr(exception, 'status_code'):
            response_data["errorCode"] = exception.error_code
            response_data["errorMessage"] = exception.message
            return HttpResponse(json.dumps(response_data), headers=headers, status=exception.status_code)
        else:
            print(traceback.print_exc())
            response_data["errorCode"] = "INTERNAL_SERVER_ERROR"
            response_data["errorMessage"] = "Internal Server Error."
            return HttpResponse(json.dumps(response_data), headers=headers, status=INTERNAL_SERVER_ERROR)