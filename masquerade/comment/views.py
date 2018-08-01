from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from user import utils
from user.models import MasUser
from .models import Comment


def create_comment(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        username = request.POST.get('username', '')
        masuserId = request.POST.get('masuserId', '')
        if token == utils.get_token(username):
            text = request.POST.get('text', '')
            masuser = MasUser.objects.get(pk=masuserId)

            content_type = request.POST.get('content_type', '')
            content_id = request.POST.get('content_id', '')

            if text and masuser and content_id and content_type:
                model_class = ContentType.objects.get(model=content_type).model_class()
                model_obj = model_class.objects.get(pk=content_id)
                comment = Comment(text=text, masuser=masuser, content_object=model_obj)

                parent_id = request.POST.get('parentId', '')
                if parent_id:
                    parent = Comment.objects.get(pk=parent_id)
                    if parent:
                        comment.parent = parent
                        # 设置当前评论的顶级评论
                        if parent.root:
                            comment.root = parent.root
                        else:
                            comment.root = parent
                comment.save()

                json = {
                    'msgCode': 666,
                    'msg': '评论发布成功'
                }
                return HttpResponse(JsonResponse(json))
            else:
                json = {
                    'msgCode': 1002,
                    'msg': '参数错误'
                }
                return HttpResponse(JsonResponse(json))
        else:
            json = {
                'msgCode': 1001,
                'msg': "token失效，请更新",
            }
            return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def get_comment(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        username = request.POST.get('username', '')
        contentType = request.POST.get('content_type', '')
        content_id = request.POST.get('content_id', '')
        if token and username and contentType and content_id:
            if token == utils.get_token(username):
                # 获取传入content_type的model类型
                content_type = ContentType.objects.get(model=contentType)
                parent_comments = Comment.objects.filter(content_type=content_type, object_id=content_id, parent=None)
                final_comments = []

                for comment in parent_comments:
                    child_comments = Comment.objects.filter(content_type=content_type, object_id=content_id, root=comment)
                    child_final_comments = []
                    if child_comments.exists():
                        for c_m in child_comments:
                            reply_to = c_m.parent.masuser.nick_name
                            cc = {
                                'comment_id': c_m.pk,
                                'comment_content': c_m.text,
                                'comment_created_time': c_m.comment_time.timestamp(),
                                'masuser': {
                                    'nick_name': MasUser.objects.get(pk=c_m.masuser.pk).nick_name
                                },
                                'reply_to_masuser': {
                                    'nick_name': reply_to,
                                }
                            }
                            child_final_comments.append(cc)
                    c_masuser = MasUser.objects.get(pk=comment.masuser.pk)
                    c = {
                        'comment_id': comment.pk,
                        'comment_content': comment.text,
                        'comment_created_time': comment.comment_time.timestamp(),
                        'masuser': {
                            'username': c_masuser.nick_name
                        },
                        'child_comments': list(child_final_comments)
                    }
                    final_comments.append(c)

                json = {
                    'comments': list(final_comments)
                }
                return HttpResponse(JsonResponse(json))
            else:
                json = {
                    'msgCode': 1001,
                    'msg': "token失效，请更新",
                }
                return HttpResponse(JsonResponse(json))
        else:
            json = {
                'msgCode': 1002,
                'msg': '参数错误'
            }
            return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))


def delete_comment(request):
    if request.method == 'POST':
        token = request.POST.get('token', '')
        masuser_name = request.POST.get('masuer_name', '')
        masuser_id = request.POST.get('masuser_id', '')
        contentType = request.POST.get('content_type', '')
        content_id = request.POST.get('content_id', '')

        if token and masuser_id and masuser_name and contentType and content_id:
            if token == utils.get_token(masuser_name):
                content_type = ContentType.objects.get(model=contentType)
                masuser = MasUser.objects.get(pk=masuser_id)
                Comment.objects.filter(content_type=content_type, pk=content_id, masuser=masuser).delete()
                json = {
                    'msgCode': 666,
                    'msg': "删除成功",
                }
                return HttpResponse(JsonResponse(json))
            else:
                json = {
                    'msgCode': 1001,
                    'msg': "token失效，请更新",
                }
                return HttpResponse(JsonResponse(json))
        else:
            json = {
                'msgCode': 1002,
                'msg': '参数错误'
            }
            return HttpResponse(JsonResponse(json))
    else:
        json = {
            'msgCode': 2001,
            'msg': "请求方法错误",
        }
        return HttpResponse(JsonResponse(json))