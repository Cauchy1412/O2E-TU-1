from django.http import HttpRequest
from core.api.utils import (ErrorCode, success_api_response, failed_api_response, wrapped_api, response_wrapper)
from core.api.auth import jwt_auth
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from core.models.image import Image
from core.models.user import User
import json


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def create_image(request: HttpRequest):
    """
    :param request:
        FILES: image: new image
    :return:
    """
    image_file = request.FILES.get("image", None)
    current_user = request.user
    if image_file is None:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "image has not provided.")

    image = Image()
    image.created_by = current_user
    image.file = image_file

    try:
        image.save()
    except Exception:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "add image error.")

    return success_api_response({
        "message": "success add a image."
    })


@response_wrapper
@jwt_auth()
@require_http_methods('PUT')
def remove_image(request: HttpRequest):
    """
    :param request:
        id: remove image id
    :return:
    """
    params = json.load(request.body.decode())

    try:
        image = Image.objects.get(pk=params.get('id', None))
    except Exception:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid image id provided.")

    try:
        image.created_by = None
        image.save()
    except Exception:
        failed_api_response(ErrorCode.SERVER_ERROR, "remove option failed.")

    return success_api_response({
        "message": "image successfully remove."
    })


@response_wrapper
@jwt_auth()
@require_http_methods('DELETE')
def delete_image(request: HttpRequest):
    """
    :param request:
        id: delete image id
    :return:
    """
    params = json.load(request.body.decode())

    try:
        image = Image.objects.get(pk=params.get('id', None))
    except Exception:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "invalid image id provided.")

    try:
        image.delete()
    except Exception:
        failed_api_response(ErrorCode.SERVER_ERROR, "delete option failed.")

    return success_api_response({
        "message": "image successfully delete."
    })


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def list_image(request: HttpRequest, pindex: int):
    """
    :param request:
        user_id: show which user
        is_global: boolean, if show all images
        num_per_page: num_per_page
    :param pindex:
        page index
    :return:
    """
    params = request.GET.dict()
    num_per_page = 20
    if params.get('num_per_page', None):
        num_per_page = int(num_per_page)
    show_user = request.user
    if params.get('user_id', None):
        try:
            user_id = int(params.get('user_id', None))
            show_user = User.objects.get(pk=user_id)
        except Exception:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "bad user_id provided.")
    image_objects = Image.objects.filter(created_by=show_user)
    if params.get('is_global', None) == 'true':
        image_objects = Image.objects.all()

    paginator = Paginator(image_objects, num_per_page)
    image_page = paginator.page(pindex)

    rst_page = []
    for image in image_page:
        rst_page.append(image.to_hash())

    return success_api_response({
        "page": rst_page,
        "has_next": image_page.has_next(),
        "has_previous": image_page.has_previous(),
        "number": image_page.number,
        "page_num": paginator.num_pages,
    })


IMAGE_API = wrapped_api({
    'POST': create_image,
    'PUT': remove_image,
    'DELETE': delete_image
})


IMAGE_SET_API = wrapped_api({
    'GET': list_image
})