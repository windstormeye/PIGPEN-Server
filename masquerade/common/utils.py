import time
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.conf import settings
from common import masLogger
from qiniu import Auth


def ErrorResponse(code, message, request):
    data = {'msgCode': code, 'msg': message}
    masLogger.log(request, 2333, message)
    return JsonResponse(data)


# 成功响应
def SuccessResponse(message, request):
    data = {'msgCode': 0, 'msg': message}
    masLogger.log(request, 0)
    return JsonResponse(data)


def get_page_blog_list(contents, page_num):
    paginator = Paginator(contents, settings.EACH_PAGE_BLOGS_NUMBER)
    page_of_contents = paginator.get_page(page_num)

    return page_of_contents


def create_upload_image_token(count):
    """
    七牛不支持多图上传，根据官方文档描述，只能在业务层循环针对每个图生成对应 token
    :param count: 需要生成的 token 个数
    :param key 文件名前缀
    :return 生成的 token 列表
    """

    jsons = []
    while count > 0:
        # 构建鉴权对象
        q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
        # 要上传的空间
        bucket_name = 'pigpen'
        token = q.upload_token(bucket_name)

        jsons.append(token)
        count -= 1

    return jsons