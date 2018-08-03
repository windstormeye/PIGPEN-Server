import logging, datetime

logger = logging.getLogger('info_logger')


def log(request, msgCode, msg=None):
    masuser_id = request.GET.get('masuser_id')
    nick_name = request.GET.get('nick_name')
    if msg:
        logger.info('%s, request=%s, path=%s, masuser_id=%s, nick_name=%s msgCode=%s, msg=%s' % (
            datetime.datetime.now(), request.get_full_path(), request.method, masuser_id, nick_name, msgCode, msg))
    else:
        logger.info('%s, request=%s, path=%s, masuser_id=%s, nick_name=%s msgCode=%s' % (
            datetime.datetime.now(), request.get_full_path(), request.method, masuser_id, nick_name, msgCode))