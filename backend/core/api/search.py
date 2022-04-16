from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from django.core.paginator import Paginator
from .utils import (failed_api_response, ErrorCode,
                    success_api_response,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from django.views.decorators.http import require_GET,require_POST
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)
from ..models import User

'web PAGE'
@response_wrapper
@jwt_auth()
@require_GET
def search_user_list(request:HttpRequest,*args, **kwargs):
    # 传入key 查找关键字
    search_key = request.GET.get("keywords")
    models = User.objects.filter(username__icontains=search_key)

    models_all = models.count()
    page = kwargs.get('page')
    page_size = kwargs.get('page_size')
    paginator = Paginator(models, page_size)
    page_all = paginator.num_pages
    #cur_user = request.user

    if page > page_all:
        models_info = []
    else:
        models_info = list(
            paginator.get_page(page).object_list.values(
                'id', 'username', 'email', 'icon', 'type','institution'
            )
        )
    data = {
        'models_all': models_all,
        'total_count': paginator.count,
        'page_all': page_all,
        'page_now': page,
        'models': models_info
    }
    return success_api_response(data)


'app ROLL'
@response_wrapper
@jwt_auth()
@require_GET
def search_user_full_list(request:HttpRequest):
    #传入key 查找关键字
    search_key = request.GET.get("key")
    models = User.objects.filter(username__icontains=search_key)
    data = list()
    cur_user = request.user
    for user in models:
        if user.is_superuser != 1:
            data.append({
                'username': user.username,
                'id': user.id,
                'email': user.email,
                'userpic': user.get_icon(),
                'nickname': user.nick_name,
                'institution': user.institution,
                'is_following' : cur_user.is_followed(user.id)
            })    
    return success_api_response(data)
