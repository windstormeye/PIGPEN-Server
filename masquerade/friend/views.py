from django.db.models import Q
from haystack.query import SearchQuerySet

from common import utils, decorator
from friend.models import Friend
from user.models import MasUser


@decorator.request_method('GET')
@decorator.request_check_args(['type'])
def getFriend(request):
    uid = request.GET.get('uid')
    type = request.GET.get('type')

    frinds = Friend.objects.filter(Q(userA__uid=uid) | Q(userB__uid=uid),
                                   status=1)
    my_frinds = []
    for frind in frinds:
        if frind.userA.uid == uid:
            my_frind = frind.userB
        else:
            my_frind = frind.userA
        if type == 0:
            my_frinds.append(my_frind.toJSON())
        else:
            # 这里需要带上宠物信息
            my_frinds.append(my_frind.toJSON())

    json = {
        'friends': my_frinds,
    }

    return utils.SuccessResponse(json, request)


@decorator.request_method('POST')
@decorator.request_check_args(['friendId', 'status'])
def addFriend(request):
    uid = request.POST.get('uid')
    friendId = request.POST.get('friendId')
    status = request.POST.get('status')

    uid_user = MasUser.objects.filter(uid=uid).first()
    friendId_user = MasUser.objects.filter(uid=friendId).first()

    if uid_user and friendId_user:
        if Friend.objects.filter(Q(userA__uid=uid)
                                 | Q(userB__uid=uid)
                                 | Q(userA__uid=uid)
                                 | Q(userB__uid=uid),
                                 status=1):
            return utils.ErrorResponse(utils.Code.existed, request)
        else:
            Friend(userA=uid_user,
                   userB=friendId_user,
                   status=status).save()
            json = {
                'status': 'ok'
            }
            return utils.SuccessResponse(json, request)
    else:
        return utils.ErrorResponse(utils.Code.notFound, request)


@decorator.request_method('GET')
@decorator.request_check_args(['s_nick_name'])
def searchFriend(request):
    nick_name = request.GET.get('s_nick_name')

    users = SearchQuerySet().models(MasUser).filter(nick_name__contains=nick_name)

    f_users = []
    for user in users:
        if user.object:
            f_users.append(user.object.toJSON())

    json = {
        'users': f_users
    }

    return utils.SuccessResponse(json, request)

