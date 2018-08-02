from functools import wraps
from . import utils


def request_methon(method):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if method == request.method:
                return func(request)
            else:
                return utils.ErrorResponse(2001, '请求方法错误')
        return wrapper
    return decorator


def request_check_args(args=None):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if request.method == 'POST':
                request_args = request.POST.dict().keys()
            else:
                request_args = request.GET.dict().keys()
            # allow multi-args
            for item in args:
                if item not in request_args:
                    return utils.ErrorResponse(1002, '参数错误')
            return func(request)
        return wrapper
    return decorator