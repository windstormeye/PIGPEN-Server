import datetime
import time
from math import radians, cos, sin, asin, sqrt
from enum import Enum, unique

from django.conf import settings
from django.core.paginator import Paginator
from django.http import JsonResponse
from qiniu import Auth

from common import masLogger


def ErrorResponse(code, request):
    code_msg = codeMsg(code.value)

    data = {'msgCode': code.value, 'msg': code_msg}
    masLogger.log(request, 2333, code_msg)
    return JsonResponse(data)


# 成功响应
def SuccessResponse(message, request):
    data = {'msgCode': Code.ok.value, 'msg': message}
    masLogger.log(request, 0)
    return JsonResponse(data)


def codeMsg(code):
    code_msg = {
        0: 'ok',
        1: 'notFound',
        2: 'existed',
        3: 'paramsError',
        4: 'methodError',
        5: 'error',
    }

    return code_msg[code]


@unique
class Code(Enum):
    """
    返回体状态码
    """
    # 正常
    ok = 0
    # 找不到
    notFound = 1
    # 已存在
    existed = 2
    # 参数错误
    paramsError = 3
    # 请求方法错误
    methodError = 4
    # 出错了
    err = 5


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
    :return: 每日所需卡路里
    """
    static_kcal = dogDayStaticKcal(weight)
    # 体重的三次方
    weight **= 3
    # 体重开方两次
    weight **= 0.5
    weight **= 0.5
    # 每日所需千卡路里
    kcal = weight * 125 - static_kcal

    return int(kcal)


def dogDayStaticKcal(weight):
    """
    狗狗一天的静息卡路里
    :param weight: 体重
    :return: 静息卡路里
    """

    weight **= 0.75
    kcal = weight * 70
    return kcal


def petTargetDrink(pet):
    """
    根据宠物体重和年龄计算每日所需水量
    :param pet: 宠物实体
    :return: 宠物每日所需水量
    """
    # 猫
    if pet.pet_type == 0:
        # 1kg * 30ml
        return pet.weight * 30
    # 狗
    else:
        total_month = (datetime.datetime.now().timestamp() - pet.created_time.timestamp()) / 86400 / 30
        # 幼年犬
        if total_month < 16:
            return pet.weight * 160
        # 成年犬
        else:
            return pet.weight * 110


def get_two_float(f_str, n):
    """
    保留任意位小数，不四舍五入
    :param f_str: 原字符串
    :param n: 小数位数
    :return: 处理完成的字符串
    """
    a, b, c = f_str.partition('.')
    c = c[:n]
    return ".".join([a, c])


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)

    :param lon1: 经度1
    :param lat1: 纬度1
    :param lon2: 经度2
    :param lat2: 纬度2
    :return: 距离（小数公里）
    """

    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine 公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里

    return c * r