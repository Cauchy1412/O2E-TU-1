from django.http import HttpRequest
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response, wrapped_api)
from core.models.notification import (Notification, UNREAD, READ)
from core.models.pap_model import PapModel
from core.models.user import User
import json

@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def create_notification(request: HttpRequest):
    """
    :param request:
        code: int, notification code
        content: string, notification content
        from_user: from user pk
        to_user: to user pk
        pap_comment: paper comment pk
    :return:
    """
    params = json.loads(request.body.decode())

    try:
        code = params.get('code', None)
        content = params.get('content', None)
        if params.get('from_user', None):
            from_user = User.objects.get(pk=params.get('from_user', None))
        else:
            from_user = request.user
        if params.get('pap_comment', None):
            mk = PapModel.objects.get(pk=params.get('pap_comment', None))
        else:
            mk = None
        to_user = User.objects.get(pk=params.get('to_user', None))
    except Exception:
        return  failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "bad params")
    if Notification.new_notification(code=code,
                                     from_user=from_user,
                                     to_user=to_user,
                                     content=content,
                                     pap_model=mk):
        return success_api_response({
            "message": "notification create successfully."
        })
    else:
        return failed_api_response(ErrorCode.SERVER_ERROR, "notification create error.")


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def get_notifications_num(request: HttpRequest):
    """
    :param request:
        only_unread: if only show unread notifications
    :return:
    """
    params = request.GET.dict()
    p = request.user

    notification_list = Notification.objects.filter(to_user=p)
    if params.get('only_unread', None) == "true":
        notification_list = notification_list.filter(read_status=UNREAD)

    return success_api_response({
        "num": len(notification_list),
    })


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def list_notifications(request: HttpRequest, pindex: int):
    """
    :param request:
        only_unread: if only show unread notifications
        num_per_page: num_per_page
    :param pindex: page number
    :return:
    """
    # some api will be used in method
    def getTime(elem):
        from datetime import datetime
        created_at_time = elem.get('created_at', None)
        if created_at_time and created_at_time.__class__ == datetime:
            return created_at_time
        else:
            return datetime.now()

    params = request.GET.dict()
    p = request.user

    num_per_page = 20
    if params.get('num_per_page', None):
        num_per_page = int(params.get('num_per_page', None))
    notification_list = Notification.objects.filter(to_user=p)
    if params.get('only_unread', None) == "true":
        notification_list = notification_list.filter(read_status=UNREAD)
    pindex = int(pindex)
    if params.get('pindex', None):
        pindex = int(params.get('pindex', None))

    paginator = Paginator(notification_list, num_per_page, allow_empty_first_page=True)
    notification_page = paginator.page(pindex)

    rst_page = []
    for notif in notification_page:
        rst = notif.to_hash()
        fid = rst.get('from_user')
        fp = User.objects.get(pk=fid)
        rst.update({
            'from_user': {
                'id': fp.id,
                'username': fp.username,
                'userpic': fp.get_icon()
            }
        })
        rst_page.append(rst)

    rst_page.sort(key=getTime)

    for notification in notification_page:
        notification.has_read()

    return success_api_response({
        "page": rst_page,
        "has_next": notification_page.has_next(),
        "has_previous": notification_page.has_previous(),
        "number": notification_page.number,
        "page_num": paginator.num_pages,
    })


NOTIFICATION_API = wrapped_api({
    'GET': get_notifications_num,
    'POST': create_notification,
})

NOTIFICATION_SET_API = wrapped_api({
    'GET': list_notifications,
})
