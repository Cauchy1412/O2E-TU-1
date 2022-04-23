"""User Management APIs
"""

from this import d
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response, wrapped_api)
from core.api.send_email import make_confirm_string, send_email, send_forget
from core.models.auth_record import AuthRecord
from core.models.user import User, ConfirmString
from core import logger
from core.models import verify_user, User, Demand,resolution

import json

@response_wrapper
@jwt_auth()
@require_GET
def recommend(request: HttpRequest):
    """set_verified

    [method]: GET

    [route]: /api/resolve/recommend
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    demand_id = data.get('demand_id')
    demand = Demand.objects.get(id=demand_id)
    expert_ids = ['41681989680','41681989680','41681989680']
    resolutions = []
    data_list = []
    for expert_id in expert_ids:
        user = User.objects.get(id=expert_id)
        verify_user = user.verified_info.first()
        resolution = resolution(demand=demand, user=user, meta=verify_user.meta)
        resolution.save()
        resolutions.append(resolution)
        data = {
            'id': resolution.id,
            'meta': json.loads(verify_user.meta),
        }
        data_list.append(data)
    re_data = {'data_list': [data for data in data_list]}
    return success_api_response(re_data)
