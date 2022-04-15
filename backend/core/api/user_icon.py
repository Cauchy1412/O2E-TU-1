from core.models.user import User
from django.http.request import HttpRequest
from core.api.utils import (require_http_methods, ErrorCode,
                            response_wrapper, wrapped_api,
                            success_api_response, failed_api_response)
from core.api.auth import jwt_auth
import os
from django.http import HttpResponse
from backend.settings import BASE_DIR

@jwt_auth()
@response_wrapper
@require_http_methods('GET')
def get_user_icon(request: HttpRequest):
    """
    get user icon
    :param request:
    :return:
    """
    p = request.user
    return success_api_response({
        "icon": str(p.get_icon()),
    })



# @jwt_auth()
# @response_wrapper
# @require_http_methods('POST')
def change_user_icon(request):
    """
    change user icon
    :param request:
        FILES: icon: new user icon
    :return:
    """
    img = request.FILES.get('files')
    user_id = request.POST.get("user")
    user = User.objects.filter(id=user_id).first()
    user.icon = img
    user.save()

    # icon = request.FILES.get("icon", None)
    # if icon is None:
    #     return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "user icon has not provided.")
    # p = request.user
    # p.icon = icon
    # try:
    #     p.save()
    # except Exception:
    #     return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "set user icon error.")
    return HttpResponse(str(user.icon))


@response_wrapper
@require_http_methods('GET')
def read_img(request:HttpRequest,year,day,file_name):
    imagepath=os.path.join(BASE_DIR,"static/images/{}/{}/icons/{}".format(year,day,file_name))
    with open(imagepath,'rb') as f:
        image_data=f.read()
    return HttpResponse(image_data,content_type="image/png")


@response_wrapper
@require_http_methods('GET')
def read_default_img(request:HttpRequest):
    imagepath=os.path.join(BASE_DIR,"static/images/default_user_icon.jpg")
    with open(imagepath,'rb') as f:
        image_data=f.read()
    return HttpResponse(image_data,content_type="image/png")



USER_ICON_API = wrapped_api({
    "GET": get_user_icon,
    "POST": change_user_icon,
})
