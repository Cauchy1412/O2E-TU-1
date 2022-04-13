"""User Management APIs
"""

from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_http_methods

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response, wrapped_api)
from core.api.send_email import make_confirm_string, send_email, send_forget
from core.models.auth_record import AuthRecord
from core.models.user import User, ConfirmString


@response_wrapper
@jwt_auth()
@require_POST
def change_password(request: HttpRequest):
    """reset password if old password matches

    [method]: POST

    [route]: /api/user/change-password
    """
    user: User = request.user
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    old_password = data.get("old-password")
    new_password = data.get("new-password")
    if old_password is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Old password required.")
    if new_password is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "New password required.")
    if not user.check_password(old_password):
        return failed_api_response(ErrorCode.REFUSE_ACCESS, "Old password not matched.")
    user.set_password(new_password)
    user.save()
    AuthRecord.objects.filter(user=user).delete()
    return success_api_response({"result": "Ok, password has been updated."})



@response_wrapper
@jwt_auth()
@require_POST
def change_email(request: HttpRequest):
    """reset email

    [method]: POST

    [route]: /api/user/change-email
    """
    user: User = request.user
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    old_email = data.get("old-email")
    new_email = data.get("new-email")
    if old_email is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Old email required.")
    if new_email is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "New email required.")
    if not user.email != old_email:
        return failed_api_response(ErrorCode.REFUSE_ACCESS, "Old email not matched.")
    user.email = new_email
    user.save()
    return success_api_response({"result": "Ok, email has been updated."})



@response_wrapper
@require_POST
def create_user(request: HttpRequest):
    """create user

    [method]: POST

    [route]: /api/user/create
    """

    data: dict = parse_data(request)

    if not data:
        print("print:wrong args in create_user")
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    email = data.get("email")
    if email is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad ID Information.")
    # if User.objects.filter(email=email).exists():
    #     return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "Email conflicted.")
    
    code = make_confirm_string(email)
    send_email(email, str(code))



    return success_api_response({'msg': 'Check code is sent'})


@response_wrapper
@require_http_methods('PUT')
def confirm_create(request: HttpRequest):
    """confirm check code

    Arguments:
        request {HttpRequest} -- PUT
    """
    data: dict = parse_data(request)
    if not data:
        print("print: not data")
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    username = data.get("username")
    password = data.get("password")
    email = data.get("email")
    code = data.get("code")
    if username is None or password is None or email is None:
        print("print : no useful agrs")
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad ID Information.")
    if User.objects.filter(username=username).exists():
        print("print : conflitc username")
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "Username conflicted.")
    if User.objects.filter(email=email).exists():
        print("print : conflitc email")
        return failed_api_response(ErrorCode.ITEM_ALREADY_EXISTS, "Email conflicted.")

    if ConfirmString.objects.filter(email=email).exists() is False:
        print("print : no confirm string")
        return failed_api_response(ErrorCode.WRONG_CONFIRM_CODE,
                                   "Invalid confirm code")
    
    confirm = ConfirmString.objects.get(email=email)
    if confirm.code != code:
        return failed_api_response(ErrorCode.WRONG_CONFIRM_CODE,
                                   "Confirm code is wrong")
    new_user = User.objects.create_user(
        username=username, password=password, email=email, is_confirmed=True)
    new_user.save()
    data = {"id": new_user.id}
    return success_api_response(data)


@response_wrapper
@require_POST
def forget_password(request: HttpRequest):
    """forget password

    Arguments:
        request {HttpRequest} -- POST

    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    email = data.get("email")
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        code = make_confirm_string(email)
        send_forget(email, str(code))
    else:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Email is not exist!")
    return success_api_response({'id': user.id})


@response_wrapper
@require_http_methods('PUT')
def confirm_forget_password(request: HttpRequest):
    """confirm forget password

    Arguments:
        request {HttpRequest} -- PUT

    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
 
    code = data.get('code')
    email = data.get("email")
    password = data.get('password')
    if code is None or email is None or password is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Please fill in all the blanks")
    if ConfirmString.objects.filter(code=code).exists() is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Invalid confirm code")
    confirm = ConfirmString.objects.get(code=code)
    if confirm.email != email:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                   "Confirm code is wrong")
    if User.objects.filter(email=email).exists() is False:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, 'Email is not exist')
    
    user = User.objects.get(email=email)
    user.set_password(password)
    user.save()

    return success_api_response({'id': user.id, 'msg': 'Update successfully'})

CREATE_USER_API = wrapped_api({
    'POST': create_user,
    'PUT': confirm_create
})

FORGET_PASSWORD_API = wrapped_api({
    "POST": forget_password,
    "PUT": confirm_forget_password
})
