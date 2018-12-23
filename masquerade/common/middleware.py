import time
from django.utils.deprecation import MiddlewareMixin
from common import token_utils, utils


class tokenCheckMiddleware(MiddlewareMixin):
    """
    Process header parameters data from GET and POST request.
    """
    @staticmethod
    def process_request(request):
        timestamp = request.META.get('HTTP_TIMESTAMP')
        if timestamp:
            now_timestamp = (time.time() - 300) / 300
            if int(timestamp) >= now_timestamp:
                if request.path != '/masuser/createmasuser' and \
                        request.path != '/masuser/login' and \
                        request.path != '/masuser/updateToken' and \
                        request.path != '/masuser/checkPhone':
                    token = request.META.get('HTTP_USERTOKEN')
                    if token:
                        username = token_utils.get_username(token)
                        if token != token_utils.get_token(username):
                            return utils.ErrorResponse(1001, 'invalid token',
                                                       request)
                    else:
                        return utils.ErrorResponse(1002, 'require token',
                                                   request)
            else:
                return utils.ErrorResponse(2333, 'timeout', request)
        else:
            return utils.ErrorResponse(1002, 'require timestamp', request)

    @staticmethod
    def process_response(request, response):
        return response