"""User Management APIs
"""

from django.http import HttpRequest
from django.views.decorators.http import require_POST

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)
from core.models.user import User
from core.models import User


@response_wrapper
@jwt_auth()
@require_POST
def set_verified(request: HttpRequest):
    """set_verified

    [method]: POST

    [route]: /api/verify/set-verify
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user_id = data.get('id')
    this_user = User.objects.get(id=user_id)
    verified_user = this_user.verified_info.all()
    for user in verified_user:
        user.set_verified()
        user.save()
    return success_api_response({"result": "set_verified sucess"})



@response_wrapper
@jwt_auth()
@require_POST
def set_failed(request: HttpRequest):
    """set_verified

    [method]: POST

    [route]: /api/verify/fail-verify
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user_id = data.get('id')
    this_user = User.objects.get(id=user_id)
    verified_user = this_user.verified_info.all()
    for user in verified_user:
        user.set_failed()
        user.save()
    return success_api_response({"result": "set failed sucess"})