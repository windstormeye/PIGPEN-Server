import time
from django.utils.deprecation import MiddlewareMixin
from common import token_utils, utils


class tokenCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        pass
        if request.path != '/masuser/createmasuser' and request.path != '/masuser/login' and request.path != '/masuser/updateToken':
            token = request.META.get('HTTP_USERTOKEN')
            timestamp = request.META.get('HTTP_TIMESTAMP')

            if token and timestamp:
                now_timestamp = (time.time() - 300) / 300
                if int(timestamp) >= now_timestamp:
                    username = token_utils.get_username(token)
                    if token == token_utils.get_token(username):
                        pass
                    else:
                        return utils.ErrorResponse(1001, 'token失效，请更新')
                else:
                    return utils.ErrorResponse(2333, '已超时')
            else:
                return utils.ErrorResponse(1002, '参数错误')

    def process_response(self, request, response):
        return response