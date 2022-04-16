from tkinter.messagebox import NO
from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.core import serializers


from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import demand, Interpretation, User

import json

@jwt_auth()
@require_POST
@response_wrapper
def create_demand(request: HttpRequest):
    """
    create demand

    [method]: POST

    [route]: /api/demand/create
    
    parms:
        - created_at: timestamp
        - title: string
        - description: string
        - meta: string
		- user: int
    """
    # import pdb
    # pdb.set_trace()
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
   	#username = data.get('username')
    user: User = request.user

    title = data.get('title')
    description = data.get('description')
    meta = json.dumps(data.get('meta'))
    
    if title is None or description is None or meta is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Key in Request.")

    interpretation_id = data.get('interpretation_id')
    content = data.get('content')

    if interpretation_id is None or content is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Key in Request.")
    if len(description) > 500 or len(title) > 100 or len(meta) > 200:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Content size too large.")
        
    demand = demand(user=user, created_at = timezone.localtime(timezone.now()), description = description, title = title, meta = meta)
    demand.save()
    ret_data = {}
    return success_api_response(ret_data)


def demand2json(demand: demand) -> dict:
    data: dict = {'user': demand.user, 
            'username': demand.user.username, 
            'user_id': demand.user.id, 
            'created_at': demand.created_at, 
            'description': demand.description, 
            'title': demand.title,
            'meta': json.loads(demand.meta),
            }
    if demand.to_user is not None:
        data['to_user']={'id': demand.to_user.id, 'username': demand.to_user.username}
    if demand.parent_demand is not None:
        data['parent_demand_id']= demand.parent_demand.id
    data['userpic'] = demand.user.icon.url
    return data

@jwt_auth()
@require_GET
@response_wrapper
def get_demand(request: HttpRequest, id: int):
    """
    get demand
    
    [method]: GET
    
    [route]: /api/demand/:id
    
    parms:
		- id: int
    """
    demand_id = id
    try:
        demand = demand.objects.get(id=demand_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    ret_data = demand2json(demand)
    return success_api_response(ret_data)

@jwt_auth()
@require_GET
@response_wrapper
def get_demand_list(request: HttpRequest):
    """
    get demand
    
    [method]: GET
    
    [route]: /api/demand
    
    parms:
    """
    data: dict = request.GET.dict()
    user = request.user
    user = User.objects.get(id = user)
    demands = user.sended_demands.all()
    re_data = {'demand_list': [demand2json(demand) for demand in demands]}
    return success_api_response(re_data)