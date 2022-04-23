from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponse

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import User, Chatroom, Message, Demand


"""
    create chatroom
    [method]: POST
    [route]: /api/chat/create

    parms:
        - chatroom_name: string
        - from_user_id: int
        - to_user_id: int
        
    return:
        - chatroom id
"""
@jwt_auth()
@require_POST
@response_wrapper
def create_chat(request: HttpRequest):

    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid request args.")
    # username = data.get('username')
    user: User = request.user

    tu_id = data.get('to_user_id')
    fr_id = data.get('from_user_id')
    chat_name = data.get('chatroom_name')
    demand_id = data.get('demand_id')

    if len(chat_name) > 30:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Chat name size too large.")

    try:
        tu = User.objects.get(id=tu_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad User ID.")

    try:
        fr = User.objects.get(id=fr_id)
    except ObjectDoesNotExist:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad User ID.")


    if tu.chatroom_list.filter(to_user_id = fr_id).exists():
        return success_api_response({'id':tu.chatroom_list.filter(to_user_id = fr_id).get().id})
    
    if fr.chatroom_list.filter(to_user_id = tu_id).exists():
        return success_api_response({'id':fr.chatroom_list.filter(to_user_id = tu_id).get().id})

    chatroom = Chatroom(name=chat_name, owner=fr, to_user=tu)
    if (demand_id):
        chatroom.demand = Demand.objects.get(id = demand_id)
    chatroom.save()
    ret_data = {'id': chatroom.id}
    return success_api_response(ret_data)




"""
    delete chat

    [method]: POST

    [route]: /api/chat/delete

    parms:
		- id: int

	return:
	    - chatroom id: int
"""
@jwt_auth()
@require_POST
@response_wrapper
def delete_chat(request: HttpRequest):
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    user: User = request.user
    chatroom_ids = data.get('cids')
    try:
        for chatroom_id in chatroom_ids:
            chatroom = Chatroom.objects.get(id=chatroom_id)
            chatroom.delete()
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Chatroom ID.")
    # if chatroom.user.id != user.id:
    #     return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Wrong user ID")
    return success_api_response({})



"""
    get comment

    [method]: GET

    [route]: /api/chat/:id

    parms:
		- id: int
	return:
	    - chatroom.to_dict()
"""
@jwt_auth()
@require_GET
@response_wrapper
def get_chat(request: HttpRequest, id: int):
    chatroom_id = id
    try:
        chatroom = Chatroom.objects.get(id=chatroom_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Chatroom ID.")
    ret_data = chatroom.to_dict()
    return success_api_response(ret_data)


"""
    get the lists of chatrooms
    [method]: GET
    [route]: /api/chat
    
    return:
       current page of chatrooms
"""
@jwt_auth()
@require_GET
@response_wrapper
def get_chat_list(request: HttpRequest):
    # data: dict = request.GET.dict()
    # if not data:
    #     return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")

    try:
        user = request.user
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid token.")
    rooms = list()
    for room in user.chatroom_list.all():
        rooms.append(room.to_dict())
    for room in user.joined_chatroom_list.all():
        rooms.append(room.to_dict())    
    # re_data = { 'owned_chatroom_list': [room.to_dict() for room in user.chatroom_list.all()],
    # 'joined_chatroom_list': [room.to_dict() for room in user.joined_chatroom_list.all()] }
    re_data = {'chatroom_list' :  rooms}
    return success_api_response(re_data)


'修改了返回值，返回消息id参数'
'还未检查合理性，即发出请求的是否为fromId'
"""
    mark the message as READ
    [method]: POST
    [route]: /api/chat/read
    parms:
        - cId: int
        - messageId: int
        - fromId: int
        - toId: int
        
    return:
       'chatroom_id': chatroom_id
        'message_id': message_id
"""
@jwt_auth()
@require_POST
@response_wrapper
def message_read(request:HttpRequest):
    #传入 cId,fromId,toId,messegeId 返回data
    data: dict = parse_data(request)
    chatroom_id = data.get('cId')
    message_id_list = data.get('messageIds')
    try:
        chatroom = Chatroom.objects.get(id=chatroom_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Chatroom ID.")

    try:
        for message_id in message_id_list:
            message = chatroom.message.all().filter(id=message_id).first()
            message.set_read()
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Message ID.")

    return success_api_response({
        'chatroom_id': chatroom_id
        })


'修改了返回值，返回消息id参数'
'还未检查合理性，即发出请求的是否为fromId'
"""
    mark the message as READ
    [method]: POST
    [route]: /api/chat/push
    parms:
        - cId: int
        - fromId: int
        - toId: int
        - content: string
        
    return:
       'chatroom_id': chatroom_id
        'message_id': message_id
"""
@jwt_auth()
@require_POST
@response_wrapper
def push_message(request:HttpRequest):
    # 传入 cId,fromId,toId,content
    data: dict = parse_data(request)
    chatroom_id = data.get('cId')
    from_user = User.objects.get(id=data.get('fromId'))
    to_user = User.objects.get(id=data.get('toId'))
    content = data.get('content')
    print(data)
    try:
        chatroom = Chatroom.objects.get(id=chatroom_id)
        message_id = Message.new_message(
                            from_user=from_user,
                            to_user=to_user,
                            content=content)
        if chatroom.add_message(message_id) is False:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Add message failed.")
        chatroom.save()
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Chatroom ID or add message failed.")

    print(message_id)
    return success_api_response({'chatroom_id': chatroom_id,'message_id': message_id})
