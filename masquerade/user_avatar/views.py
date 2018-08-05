import os
from .models import UserAvatar
from common import decorator, utils, masLogger
from user.models import MasUser


@decorator.request_methon('POST')
@decorator.request_check_args([])
def upload_avatar(request):
    masuser_id = request.POST.get('masuser_id')
    avatar = request.FILES.get('avatar')
    if avatar:
        masuser = MasUser.objects.get(pk=masuser_id)

        if not UserAvatar.objects.filter(masuser=masuser):
            user_avatar = UserAvatar(masuser=masuser, avatar=avatar)
            user_avatar.save()

            json = {
                'masuser_id': masuser_id,
                'avatar': user_avatar.avatar.url,
            }

            masLogger.log(request, 666)
            return utils.SuccessResponse(json)
        else:
            masLogger.log(request, 2333, '用户头像已存在')
            return utils.ErrorResponse(2333, '用户头像已存在')
    else:
        return utils.ErrorResponse(2333, '请上传图片')


@decorator.request_methon('POST')
@decorator.request_check_args([])
def update_avatar(request):
    masuser_id = request.POST.get('masuser_id')
    avatar = request.FILES.get('avatar')

    if avatar:
        masuser = MasUser.objects.get(pk=masuser_id)

        if UserAvatar.objects.filter(masuser=masuser).exists():
            old_avatar = UserAvatar.objects.get(masuser=masuser)
            # delete from disk
            os.remove(old_avatar.avatar.path)
            # delete from db
            old_avatar.delete()

            new_avatar = UserAvatar(masuser=masuser, avatar=avatar)
            new_avatar.save()

            json = {
                'masuser_id': masuser_id,
                'avatar': new_avatar.avatar.url,
            }
            masLogger.log(request, 666)
            return utils.SuccessResponse(json)
        else:
            masLogger.log(request, 2333, '用户头像不存在')
            return utils.ErrorResponse(2333, '用户头像不存在')
    else:
        masLogger.log(request, 2333, '请上传图片')
        return utils.ErrorResponse(2333, '请上传图片')