from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.exceptions import ObjectDoesNotExist


from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import Demand, User
from core import logger

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
    data: dict = parse_data(request)
    user: User = request.user

    title = data['title']
    description = data['description']
    meta = json.dumps(data['meta'])

    demand = Demand(user=user, description=description, title=title, meta=meta)
    demand.save()
    return success_api_response(None)


def demand2json(demand: Demand) -> dict:
    verified_user = demand.user.verified_info.first()
    data = {
        'id' : demand.id,
        'user': {
            'id': demand.user.id,
            'username': demand.user.username,
        },
        'company_meta' : json.loads(verified_user.meta) if verified_user else None,
        'created_at': demand.created_at,
        'description': demand.description,
        'title': demand.title,
        'meta': json.loads(demand.meta),
        'state': demand.state,
    }

    try:
        if demand.to_user is not None:
            data['to_user']={'id': demand.to_user.id, 'username': demand.to_user.username}
        if demand.parent_demand is not None:
            data['parent_demand_id']= demand.parent_demand.id
    except:
        logger.error('demand2json: skipping unimplemented fields')
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
    user = request.user
    demands = user.sended_demands.all()
    re_data = {'demand_list': [demand2json(demand) for demand in demands]}
    return success_api_response(re_data)

@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def get_all_demands(request: HttpRequest):
    demands = Demand.objects.all()
    data = {'demand_list': [demand2json(demand) for demand in demands]}
    return success_api_response(data)

@jwt_auth()
@require_POST
@response_wrapper
def update_demand_state(request: HttpRequest):
    """
    update demand state

    [method]: POST

    [route]: /api/demand/update-demand-state

    parms:
        - id
        - state
    """
    data: dict = parse_data(request)
    if not data:
        print("print: not data")
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    id = data.get('id')
    state = data.get('state')
    try:
        demand = Demand.objects.get(id=id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    demand.state = state
    demand.save()
    return success_api_response({'msg': 'Resolution state is updated'})

@jwt_auth()
@require_POST
@response_wrapper
def update_demand_info(request: HttpRequest):
    """
    update demand info

    [method]: POST

    [route]: /api/demand/update-demand-info

    parms:
        - id
        - state
    """
    data: dict = parse_data(request)
    if not data:
        print("print: not data")
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    description = data.get('description')
    title = data.get('title')
    meta = data.get('meta')
    id = data.get('id')
    try:
        demand = Demand.objects.get(id=id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    demand.description = description
    demand.title = title
    demand.meta = json.dumps(meta)
    demand.save()
    return success_api_response({'msg': 'Resolution state is updated'})

@jwt_auth()
@require_POST
@response_wrapper
def delete_demand(request: HttpRequest):
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    id = data.get('id')
    try:
        demand = Demand.objects.get(id=id)
        resolutions = demand.resolutions.all()
        for resolution in resolutions:
            resolution.delete()
        chatrooms = demand.demand_rooms.all()
        for chatroom in chatrooms:
            chatroom.delete()
        demand.delete()

    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Chatroom ID.")
    return success_api_response({})

