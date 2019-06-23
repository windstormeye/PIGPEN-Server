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
    """
    对集合进行分页（不管集合内容的类型）
    :param contents: 集合内容
    :param page_num: 当前分页
    """
    paginator = Paginator(contents, settings.EACH_PAGE_BLOGS_NUMBER)
    page_of_contents = paginator.get_page(page_num)

    return page_of_contents


def create_upload_image_token(count, key):
    """
    七牛不支持多图上传，根据官方文档描述，只能在业务层循环针对每个图生成对应 token
    :param count: 需要生成的 token 个数
    :param key: 文件名前缀
    :return 生成的 token 列表
    """

    jsons = []
    while count > 0:
        # 构建鉴权对象
        q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
        # 要上传的空间
        bucket_name = 'pigpen'
        # 文件名
        k = bucket_name + key + str(int(time.time())) + str(count) + '.jpeg'
        token = q.upload_token(bucket_name, k)

        json = {
            'img_token': token,
            'img_key': k
        }

        jsons.append(json)
        count -= 1

    return jsons


def create_full_image_url(keys):
    """
    拼接获取完成后的图片 url
    :param keys: 从客户端发送来的 keys，遍历出的每一个 key 代表一个文件名
    :return image_urls: 返回拼接完成后的图片 url 数组
    """
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)
    bucket_name = 'pigpenimg.pjhubs.com'

    image_urls = []
    for index, key in enumerate(keys):
        base_url = 'http://%s/%s' % (bucket_name, key)
        private_url = q.private_download_url(base_url, expires=3600)

        image_urls.append(private_url)

    return image_urls


def dogDayTargetKcal(weight):
    """
    狗一天所需卡路里
    :param weight: 体重
    :return: 卡路里
    """

    # 体重的三次方
    weight **= 3
    # 体重开方两次
    weight **= 0.5
    weight **= 0.5
    # 每日所需千卡路里
    kcal = weight * 125

    return int(kcal)
