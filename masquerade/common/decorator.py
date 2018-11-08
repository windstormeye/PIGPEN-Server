from functools import wraps
from . import utils


def request_methon(method):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if method == request.method:
                return func(request)
            else:
                return utils.ErrorResponse(2001, '请求方法错误', request)

        return wrapper

    return decorator


'''
    @description    every API should put `masuser_id` and `nick_name` keys.
                    If args=None, should put null list, e.g: []    
'''


def request_check_args(args=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if request.method == 'POST':
                request_args = request.POST.dict().keys()
            else:
                request_args = request.GET.dict().keys()
            # allow multi-args
            args.append('nick_name')
            for item in args:
                if item not in request_args:
                    return utils.ErrorResponse(1002, '参数错误', request)
            return func(request)

        return wrapper

    return decorator
