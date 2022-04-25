from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from django.core.paginator import Paginator
from .utils import (failed_api_response, ErrorCode,
                    success_api_response, parse_data,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from core.models.notification import (Notification, USER_FOLLOW)
from core.models.user import User
from core.models.interpretation import Interpretation
from .auth import getUserInfo
# follow apis

@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def follow(request: HttpRequest, pid: int):
    """ follow someone
    :param request: http request
    :param pid: follow user id
    :return:
    """
    user = request.user
    _success = user.follow_by_id(pid)
    Notification.new_notification(
        code=USER_FOLLOW,
        from_user=user,
        to_user=User.objects.get(pk=pid),
        content="Congratulation! you have a new fan")

    if _success:
        return success_api_response({})
    else:
        return failed_api_response({"code":0})


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def unfollow(request: HttpRequest, pid: int):
    """ follow someone
    :param request: http request
    :param pid: follow user id
    :return:
    """
    user = request.user
    _success = user.unfollow_by_id(pid)
    if _success:
        return success_api_response({})
    else:
        return failed_api_response({"code":0})


""" 
    get favorite list
    :param request:
        num_per_page: num_per_page
    :param pindex: which page
    return:
        lists of follower recent 
"""
@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def list_favorite_recent(request: HttpRequest, pindex: int):

    def getTime(elem):
        from datetime import datetime
        created_at_time = elem.get('created_at', None)
        if created_at_time and created_at_time.__class__ == datetime:
            return created_at_time
        else:
            return datetime.now()
    # basic params
    params = request.GET.dict()

    num_per_page = 20
    if params.get('num_per_page', None):
        num_per_page = int(params.get('num_per_page', None))
    if num_per_page <= 0:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "num_per_page should be bigger than 0.")

    user = request.user

    recent_list = []
    if params.get('interpretation', None) == 'true':
        inter_list = Interpretation.objects.filter(pk__in=user.collect_list.values_list('id', flat=True))
        for inter in inter_list:
            rst = inter.to_hash(current_user=user)
            recent_list.append(rst)

    recent_list.sort(key=getTime, reverse=True)
    # paginate
    paginator = Paginator(recent_list, num_per_page)
    recent_page = paginator.page(pindex)

    # import pdb
    # pdb.set_trace()
    return success_api_response({
        "page": list(recent_page),
        "has_next": recent_page.has_next(),
        "has_previous": recent_page.has_previous(),
        "number": recent_page.number,
        "page_num": paginator.num_pages,
    })



@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def change_organization(request: HttpRequest):
    """reset institution
    [method]: POST
    [route]: /api/user/organization
    """
    user: User = request.user
    # import pdb
    # pdb.set_trace()
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    institution = data.get("organization")
    if institution is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Instituion required.")
    if len(institution) > 20:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Your Instituion name is too large!")

    user.institution = institution
    user.save()
    return success_api_response({"result": "Ok, your instituition has been updated."})


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def get_all_user_info(request: HttpRequest):
    models = User.objects.all()
    data = list()
    for user in models:
        if user.is_superuser != 1:
            data.append(getUserInfo(user))    
    return success_api_response(data)


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def delete_user(request: HttpRequest):
    data: dict = parse_data(request)
    pid = data.get('id')
    if User.objects.filter(pk=pid).exists() is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,'Your required user to delete is not found!')
    user = User.objects.filter(pk=pid).first()
    User.objects.get(pk=pid).delete()
    return success_api_response({"result": "Ok, all user info has been provided."})

@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def change_user_info(request: HttpRequest):
    #TODO
    data: dict = parse_data(request)
    pid = data.get('id')
    institution = data.get('institution')
    username = data.get('name')
    email = data.get('mail')
    usertype = data.get('usertype')
    if User.objects.filter(pk=pid).exists() is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,'Your required user to change is not found!')
    if User.objects.filter(username=username).exists():
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "Username conflicted.")
    if User.objects.filter(email=email).exists():
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "Email conflicted.")
    user =  User.objects.filter(pk=pid).first()
    user.username = username
    user.institution = institution
    user.email = email
    if isinstance(usertype, int) is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,'Your user type should be an int.')
    user.user_type = usertype
    user.save()
    return success_api_response({"result": "Ok, the user info has been changed."})

@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def get_user_info(request: HttpRequest):
    data: dict = parse_data(request)
    user_id = data.get('id')
    user = User.objects.get(id = user_id)
    return success_api_response(getUserInfo(user))