from functools import wraps
from . import utils


def request_method(method):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if method == request.method:
                return func(request)
            else:
                return utils.ErrorResponse(utils.Code.methodError, request)

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
            args.append('nick_name')
            args.append('uid')
            for item in args:
                if item not in request_args and item == '':
                    return utils.ErrorResponse(utils.Code.paramsError, request)
            return func(request)

        return wrapper

    return decorator
