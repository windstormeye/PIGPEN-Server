from functools import wraps
from . import utils


def request_methon(method):
    def decorator(func):
        @wraps(func)
        def wrapper(request):
            if method == request.method:
                return func(request)
            else:
                return utils.ErrorResponse(2001, 'request method error', request)

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
                if item not in request_args and item != '':
                    return utils.ErrorResponse(1002,
                                               'require % s' % item,
                                               request)
            return func(request)

        return wrapper

    return decorator
