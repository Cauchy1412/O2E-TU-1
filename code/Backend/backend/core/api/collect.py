from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from django.core.paginator import Paginator
from .utils import (failed_api_response, ErrorCode,
                    success_api_response,
                    wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from core.models.micro_evidence import MicroEvidence
from core.models.micro_conjecture import MicroConjecture
from core.models.notification import (Notification, USER_FOLLOW)
from django.views.decorators.http import require_GET,require_POST
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)
from datetime import datetime

@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def createCollect(request: HttpRequest):
    data : dict = parse_data(request)
    id = data.get("id") # 论文解读id
    uid = data.get("uid") # 用户id
    ret = {
        'id': 233,  # main key id of interpretation
    }
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('DELETE')
def deleteCollect(request: HttpRequest):
    data: dict = parse_data(request)
    user = request.user
    ids = data.get("ids") #用户要删除收藏的论文解读id数组
    ret = {}
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def getCollect(request: HttpRequest):
    user = request.user #获取该用户的收藏，返回值与获取推荐论文解读相同
    ret = {}
    return success_api_response(ret)


INTERPRETATION_COLLECT_API = wrapped_api({
    'DELETE': deleteCollect,
    'POST': createCollect,
    'GET': getCollect,
})