from django.utils.deprecation import MiddlewareMixin
from common import token_utils, utils


class tokenCheckMiddleware(MiddlewareMixin):

    def process_request(self, request):
        token = request.META.get('HTTP_USERTOKEN')

        if token:
            username = token_utils.get_username(token)
            if token == token_utils.get_token(username):
                pass
            else:
                return utils.ErrorResponse(1001, 'token失效，请更新')
        else:
            return utils.ErrorResponse(1002, '参数错误')

    def process_response(self, request, response):
        return response