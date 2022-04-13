from core.models.tag import (Tag, TAG)
from core.api.utils import (wrapped_api, response_wrapper, success_api_response, failed_api_response)
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from django.core.paginator import Paginator


@response_wrapper
@require_http_methods('GET')
def list_tags(request: HttpRequest, pindex):
    """
    get a page
    :param request:
        keywords: list of string
        num_per_page: num_per_page
        presupposed: if only need TAG
    :param pindex: page index
    :return:
    """
    params = request.GET.dict()
    tag_list = Tag.objects.none()
    keywords = params.get('keywords', None)
    if keywords:
        for keyword in keywords:
            tag_list = tag_list | Tag.objects.filter(name__icontains=keyword)
    else:
        tag_list = Tag.objects.all()
    if params.get('presupposed'):
        tag_list = tag_list.filter(type=TAG)
    num_per_page = 20
    if params.get('num_per_page', None):
        num_per_page = int(params.get('num_per_page', None))
    paginator = Paginator(tag_list, num_per_page)
    tag_page = paginator.page(pindex)
    page_json = []
    for item in tag_page.object_list:
        rst = item.to_hash()
        page_json.append(rst)
    return success_api_response({
        "page": page_json,
        "has_next": tag_page.has_next(),
        "has_previous": tag_page.has_previous(),
        "number": tag_page.number,
        "page_num": paginator.num_pages,
    })


TAG_SET_API = wrapped_api({
    'GET': list_tags
})
