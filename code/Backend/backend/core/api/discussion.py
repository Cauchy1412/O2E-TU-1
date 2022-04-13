from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.core import serializers


from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import Topic, Discussion, User

@jwt_auth()
@require_POST
@response_wrapper
def create_discussion(request: HttpRequest):
    """
    create discussion

    [method]: POST

    [route]: /api/discussion/create
    
    parms:
		- topic_id: int
		- content: string
        - to_user_id: int
        - parent_discussion_id: int
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
   	#username = data.get('username')
    user: User = request.user
    topic_id = data.get('topic_id')
    content = data.get('content')
    tu_id = data.get('to_user_id')
    pd_id = data.get('parent_discussion_id')
    if topic_id is None or content is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Key in Request.")
    if len(content) > 500:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Content size too large.")
    try:
        topic = Topic.objects.get(id=topic_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad post ID.")
    if tu_id is None:
        tu = None
    else:
        try:
            tu = User.objects.get(id=tu_id)
        except ObjectDoesNotExist:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad User ID.")
        
    if pd_id is None:
        pd = None
    else:
        try:
            pd = topic.discussion_list.get(id = pd_id)
        except ObjectDoesNotExist:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Comment ID.")
    discussion = Discussion(topic=topic, user=user, text=content, to_user=tu, parent_discussion = pd)
    discussion.save()
    ret_data = {'id': discussion.id}
    return success_api_response(ret_data)

@jwt_auth()
@require_POST
@response_wrapper
def delete_discussion(request: HttpRequest):
    """
    delete comment
    
    [method]: POST
    
    [route]: /api/discussion/delete
    
    parms:
		- id: int
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user: User = request.user
    discussion_id = data.get('id')
    try:
        discussion = Discussion.objects.get(id=discussion_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    if discussion.user.id != user.id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Wrong user ID")
    discussion.delete()
    return success_api_response({'id': discussion_id})

@jwt_auth()
@require_GET
@response_wrapper
def get_discussion(request: HttpRequest, id: int):
    """
    get comment
    
    [method]: GET
    
    [route]: /api/discussion/:id
    
    parms:
		- id: int
    """
    discussion_id = id
    try:
        discussion = Discussion.objects.get(id=discussion_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    ret_data = discussion.to_dict()
    return success_api_response(ret_data)

@jwt_auth()
@require_GET
@response_wrapper
def get_discussion_list(request: HttpRequest):
    """
    get discussion
    
    [method]: GET
    
    [route]: /api/discussion
    
    parms:
        - topic_id: int
		- pindex: int 
        - psize: int
    """
    data: dict = request.GET.dict()
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    else:
        topic_id = data.get('topic_id')
        pindex = data.get('pindex')
        psize = data.get('psize')
    if topic_id is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    if pindex is None:
        pindex = 1
    if psize is None:
        psize = 20
    try:
        topic = Topic.objects.get(id = topic_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid micro knowledge id.")
    paginator = Paginator(topic.discussion_list.all(), psize)
    try:
        cp = paginator.page(pindex)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad page args.")
    re_data = {'topic_list': [topic.to_dict() for topic in cp.object_list], 'page_count': paginator.num_pages}
    return success_api_response(re_data)