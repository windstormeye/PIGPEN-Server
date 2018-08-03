from django.contrib.contenttypes.models import ContentType
from user.models import MasUser
from .models import Comment
from common import utils, decorator, masLogger


@decorator.request_methon('POST')
@decorator.request_check_args(['content_type', 'content_id', 'text'])
def create_comment(request):
    masuserId = request.POST.get('masuser_id', '')
    text = request.POST.get('text', '')
    content_type = request.POST.get('content_type', '')
    content_id = request.POST.get('content_id', '')

    masuser = MasUser.objects.get(pk=masuserId)

    model_class = ContentType.objects.get(model=content_type).model_class()
    model_obj = model_class.objects.get(pk=content_id)
    comment = Comment(text=text, masuser=masuser, content_object=model_obj)

    parent_id = request.POST.get('parent_id', '')
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

    masLogger.log(request, 666, '评论发布成功')
    return utils.SuccessResponse('评论发布成功')


@decorator.request_methon('POST')
@decorator.request_check_args(['content_type', 'content_id'])
def get_comment(request):
    contentType = request.POST.get('content_type', '')
    content_id = request.POST.get('content_id', '')

    content_type = ContentType.objects.get(model=contentType)
    parent_comments = Comment.objects.filter(content_type=content_type, object_id=content_id, parent=None)
    final_comments = []

    for comment in parent_comments:
        # get child comment
        child_comments = Comment.objects.filter(content_type=content_type, object_id=content_id, root=comment).order_by('comment_time')
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
    masLogger.log(request, 666)
    return utils.SuccessResponse(json)


@decorator.request_methon('POST')
@decorator.request_check_args(['content_type', 'content_id'])
def delete_comment(request):
    masuser_id = request.POST.get('masuser_id', '')
    contentType = request.POST.get('content_type', '')
    content_id = request.POST.get('content_id', '')

    content_type = ContentType.objects.get(model=contentType)
    masuser = MasUser.objects.get(pk=masuser_id)
    Comment.objects.filter(content_type=content_type, pk=content_id, masuser=masuser).delete()

    masLogger.log(request, 666, '删除成功')
    return utils.SuccessResponse('删除成功')