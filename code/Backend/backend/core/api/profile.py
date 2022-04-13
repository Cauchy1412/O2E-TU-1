
from core.models.interpretation import Interpretation
from django.http import HttpRequest
from django.views.decorators.http import require_GET
from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)
from core.models.user import User


@response_wrapper
@jwt_auth()
@require_GET
def get_profile(request: HttpRequest):
    data: dict = request.GET.dict()
    user = request.user
    print(user.id)
    if data is not None:
        user_id = data.get('user_id')
        if user_id is not None:
            if User.objects.filter(pk=user_id).exists() is False:
                return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                           'User is not exist')
            user = User.objects.get(pk=user_id)

    all_post = user.created_by.all().distinct()
    total_like = 0
    total_collect = 0
    total_comment = 0

    for post in all_post:
        total_like += post.likers.count()
        total_collect += post.collectors.count()
        if post.id in Interpretation.objects.values_list('pk', flat=True):
            interpretation = Interpretation.objects.filter(pk=post.id).all()[0]
            total_comment += interpretation.comment_list.count()

    total_mycollect = 0

    for interpretation in Interpretation.objects.all():
        if user in interpretation.collectors.all():
            total_mycollect += 1

    
    data = {
        'id': user.id,
        'username': user.username,
        'nickname': user.nick_name,
        'userpic': str(user.icon),
        'email': user.email,
        'type' : user.user_type,
        'institution': user.institution,
        'total_post': user.created_by.count(),
        'total_like': total_like,
        'total_collect': total_collect,
        'total_comment': total_comment,
        'total_mycollect': total_mycollect,
        'total_fan': user.user_set.count(),
        'total_follow': user.followers.count(),
        'is_following': user.user_set.filter(id=request.user.id).exists(),
        'is_followed': user.followers.filter(id=request.user.id).exists()
    }
    return success_api_response(data)

