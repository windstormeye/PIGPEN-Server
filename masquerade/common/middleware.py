import time
from django.utils.deprecation import MiddlewareMixin
from common import token_utils, utils


class tokenCheckMiddleware(MiddlewareMixin):
    def process_request(self, request):
        timestamp = request.META.get('HTTP_TIMESTAMP')
        token = request.META.get('HTTP_USERTOKEN')
        if timestamp is not None and token is not None:
            now_timestamp = (time.time() - 300) / 300
            if int(timestamp) >= now_timestamp:
                if request.path != '/masuser/createmasuser' and \
                        request.path != '/masuser/login' and \
                        request.path != '/masuser/updateToken' and \
                        request.path != '/masuser/checkPhone':
                    if token:
                        username = token_utils.get_username(token)
                        if token != token_utils.get_token(username):
                            return utils.ErrorResponse(1001,
                                                       'token失效，请更新',
                                                       request)
                    else:
                        return utils.ErrorResponse(1001,
                                                   'token失效，请更新',
                                                   request)
            else:
                return utils.ErrorResponse(2333, '已超时', request)
        else:
            return utils.ErrorResponse(1002, '参数错误', request)

    def process_response(self, request, response):
        return response