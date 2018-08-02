from django.http import JsonResponse


def ErrorResponse(code, message):
    data = {}
    data['msgCode'] = code
    data['msg'] = message
    return JsonResponse(data)


def SuccessResponse(message):
    data = {}
    data['msgCode'] = '666'
    data['msg'] = message
    return JsonResponse(data)