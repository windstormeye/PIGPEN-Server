from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from common import masLogger


def ErrorResponse(code, message, request):
    data = {'msgCode': code, 'msg': message}
    masLogger.log(request, 2333, message)
    return JsonResponse(data)


# 成功响应
def SuccessResponse(message, request):
    data = {'msgCode': 666, 'msg': message}
    masLogger.log(request, 666)
    return JsonResponse(data)


def get_page_blog_list(contents, page_num):
    paginator = Paginator(contents, settings.EACH_PAGE_BLOGS_NUMBER)
    page_of_contents = paginator.get_page(page_num)

    return page_of_contents
