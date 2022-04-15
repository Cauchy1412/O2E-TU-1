from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.core import serializers

from datetime import datetime


from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response, wrapped_api)

from core.models import Project, User, Timeline


@jwt_auth()
@require_POST
@response_wrapper
def create_timeline(request: HttpRequest):
    """
    [method]: POST
    [path]: /timeline/create
    """
    user = request.user
    data = parse_data(request)
    time_string = data.get('time')
    event = data.get('event')
    pid = data.get('project_id')
    if time_string is None or event is None or pid is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "BAD ARGS.")
    time = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
    try:
        project = Project.objects.get(id=pid)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "BAD project id.")
    timeline = Timeline(time=time, event=event, project=project)
    timeline.save()
    return success_api_response({'id': timeline.id})


@jwt_auth()
@require_POST
@response_wrapper
def update_timeline(request: HttpRequest, id: int):
    """
    [method]: POST

    [path]: /timeline/<id: int>
    """
    data = parse_data(request)
    time_string = data.get('time')
    event = data.get('event')
    try:
        timeline = Timeline.objects.get(id=id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "ID NOT EXIST.")
    if timeline.project.create_user != request.user:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "BAD USER.")
    if time_string is not None:
        time = datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
        timeline.time = time
    if event is not None:
        timeline.event = event
    timeline.save()
    return success_api_response({})


@jwt_auth()
@require_GET
@response_wrapper
def get_timeline(request: HttpRequest, id: int):
    """
    [method]: GET

    [path]: /timeline/<id: int>
    """
    try:
        timeline = Timeline.objects.get(id=id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "ID NOT EXIST.")
    return success_api_response(timeline.to_dict())


@jwt_auth()
@require_http_methods('DELETE')
@response_wrapper
def delete_timeline(request: HttpRequest, id: int):
    try:
        timeline = Timeline.objects.get(id=id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "ID NOT EXIST.")
    if timeline.project.create_user != request.user:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "BAD USER.")
    timeline.delete()
    return success_api_response({})


@jwt_auth()
@require_GET
@response_wrapper
def get_timeline_list(request: HttpRequest):
    """
    get comment

    [method]: GET

    [route]: /api/timeline
    """
    data: dict = request.GET.dict()
    if data:
        project_id = data.get('project_id')
        pindex = data.get('pindex')
        psize = data.get('psize')
    else:
        project_id = None
        pindex = None
        psize = None
    if pindex is None:
        pindex = 1
    if psize is None:
        psize = 20
    query = Timeline.objects.all()
    if project_id is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, 'BAD ARGS.')
    query = query.filter(project__id=project_id)
    query.order_by('time')
    paginator = Paginator(query, psize)
    try:
        cp = paginator.page(pindex)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad page args.")
    re_data = {'timeline_list': [
        timeline.to_dict() for timeline in cp.object_list], 'page_count': paginator.num_pages}
    return success_api_response(re_data)


TIMELINE_API = wrapped_api({
    'POST': update_timeline,
    'GET': get_timeline,
    'DELETE': delete_timeline,
})
