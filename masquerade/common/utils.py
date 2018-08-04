from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings


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


def get_page_blog_list(contents, page_num):
    paginator = Paginator(contents, settings.EACH_PAGE_BLOGS_NUMBER)
    page_of_contents = paginator.get_page(page_num)

    return page_of_contents