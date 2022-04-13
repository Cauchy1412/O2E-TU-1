from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.core import serializers


from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import Comment, Interpretation, User

@jwt_auth()
@require_POST
@response_wrapper
def create_comment(request: HttpRequest):
    """
    create comment

    [method]: POST

    [route]: /api/comment/create
    
    parms:
		- interpretation_id: int
		- content: string
        - to_user_id: int
        - parent_comment_id: int
    """
    # import pdb
    # pdb.set_trace()
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
   	#username = data.get('username')
    user: User = request.user
    interpretation_id = data.get('interpretation_id')
    content = data.get('content')
    tu_id = data.get('to_user_id')
    pc_id = data.get('parent_comment_id')
    if interpretation_id is None or content is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Key in Request.")
    if len(content) > 500:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Content size too large.")
    try:
        interpretation = Interpretation.objects.get(pk=interpretation_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Interpretation ID.")
    if tu_id is None:
        tu = None
    else:
        try:
            tu = User.objects.get(id=tu_id)
        except ObjectDoesNotExist:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad User ID.")
        
    if pc_id is None:
        pc = None
    else:
        try:
            pc = interpretation.comment_list.get(id = pc_id)
        except ObjectDoesNotExist:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Comment ID.")
    #if (pc is None)^(tu is None):
    #    return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad parent Comment and to User.")
    comment = Comment(interpretation = interpretation, user=user, created_at = timezone.localtime(timezone.now()), text=content, to_user=tu, parent_comment = pc)
    comment.save()
    ret_data = {'id': comment.pk}
    return success_api_response(ret_data)

@jwt_auth()
@require_POST
@response_wrapper
def delete_comment(request: HttpRequest):
    """
    delete comment
    
    [method]: POST
    
    [route]: /api/comment/delete
    
    parms:
		- id: int
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user: User = request.user
    comment_id = data.get('id')
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    if user.is_superuser != 1 and comment.user.id != user.id:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Wrong user ID")
    comment.delete()
    return success_api_response({'id': comment_id})

def comment2json(comment: Comment) -> dict:
    data: dict = {'id': comment.id, 
            'username': comment.user.username, 
            'user_id': comment.user.id, 
            'created_at': comment.created_at, 
            'text': comment.text, 
            'interpretation_id': comment.interpretation.id,
            }
    if comment.to_user is not None:
        data['to_user']={'id': comment.to_user.id, 'username': comment.to_user.username}
    if comment.parent_comment is not None:
        data['parent_comment_id']= comment.parent_comment.id
    data['userpic'] = comment.user.icon.url
    return data

@jwt_auth()
@require_GET
@response_wrapper
def get_comment(request: HttpRequest, id: int):
    """
    get comment
    
    [method]: GET
    
    [route]: /api/comment/:id
    
    parms:
		- id: int
    """
    comment_id = id
    try:
        comment = Comment.objects.get(id=comment_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    ret_data = comment2json(comment)
    return success_api_response(ret_data)

@jwt_auth()
@require_GET
@response_wrapper
def get_comment_list(request: HttpRequest):
    """
    get comment
    
    [method]: GET
    
    [route]: /api/comment
    
    parms:
        - interpretation_id: int
		- pindex: int 
        - psize: int
    """
    data: dict = request.GET.dict()
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    else:
        mk_id = data.get('interpretation_id')
        pindex = data.get('pindex')
        psize = data.get('psize')
    if mk_id is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    if pindex is None:
        pindex = 1
    if psize is None:
        psize = 20
    try:
        mk = Interpretation.objects.get(id = mk_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid interpretation id.")
    paginator = Paginator(mk.comment_list.all(), psize)
    try:
        cp = paginator.page(pindex)
    except:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad page args.")
    re_data = {'comment_list': [comment2json(comment) for comment in cp.object_list], 'page_count': paginator.num_pages}
    return success_api_response(re_data)
    #cl = list(cp.object_list.values())
    #return success_api_response({'comment_list': cl, 'page_count': paginator.count})