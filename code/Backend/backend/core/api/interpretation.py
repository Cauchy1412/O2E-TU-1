import os
import bs4
from django.http.response import FileResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest
from django.core.paginator import Paginator
from .utils import (failed_api_response, ErrorCode,
                    success_api_response,
                    wrapped_api, response_wrapper,
                    parse_data)
from core.api.auth import jwt_auth
from core.models.notification import (Notification, USER_FOLLOW, PAP_COMMENT_LIKE, PAP_COMMENT_RELEASE)
from core.models.interpretation import Interpretation
from core.models.tag import Tag, TAG, KEYWORD
from core.models.keyword import Keyword
from django.views.decorators.http import require_GET,require_POST
from django.db.models import Q
from datetime import datetime
import pdfkit
from backend.settings import PDF_CACHE_DIR
import random
from bs4 import BeautifulSoup

def filter_unsafe(string: str):
    soup = BeautifulSoup(string, "html.parser")
    for _html_tag in soup.find_all():
        if _html_tag.name == 'script':
            _html_tag.decompose()
    return str(soup)

@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def createInterpretation(request: HttpRequest):
    # import pdb
    # pdb.set_trace()
    data: dict = parse_data(request)
    user = request.user

    content: str = filter_unsafe(data.get('content'))
    citation: str = filter_unsafe(data.get('citation'))
    source: str = filter_unsafe(data.get('source'))
    publish_year: int = data.get('published_year')
    title: str = filter_unsafe(data.get('title'))
    tags: list = data.get('tags')

    # import pdb
    # pdb.set_trace()
    this_interpretation = Interpretation()
    this_interpretation.content = content
    this_interpretation.created_by = user
    this_interpretation.title = title
    this_interpretation.publish_year = publish_year
    this_interpretation.save()
    for _tag in tags:
        _tag_name, _tag_type = _tag['name'], _tag['type']
        _tag_matches = Tag.objects.filter(name=_tag_name.lower())
        if _tag_matches.count() > 0:
            _tag_model = _tag_matches.all()[0]
        else:
            _tag_model = Tag(name=_tag_name.lower(), type=_tag_type)
            _tag_model.save()
        this_interpretation.add_tag(_tag_model)
        pass
    this_interpretation.source = source
    this_interpretation.citation = citation

    this_interpretation.save()

    # notify followers
    for follower_user in user.user_set.all():
        # import pdb
        # pdb.set_trace()
        Notification.new_notification(
            code=PAP_COMMENT_RELEASE,
            from_user=user,
            to_user=follower_user,
            content="Created an interpretation",
            pap_model=this_interpretation
        )

    # print(f'[DEBUG] current interpretation @ {this_interpretation.to_hash()}')

    ret = {
        'id': this_interpretation.pk,  # main key id of interpretation
    }
    print('[DEBUG] Successfully create Interpretation msg.')
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('DELETE')
def deleteInterpretation(request: HttpRequest, id: int):
    user = request.user
    
    #id 为要删除的论文解读id
    this_interpretation = Interpretation.objects.get(pk=id)

    # identity check
    if user.is_superuser == 0 and user != this_interpretation.created_by:
        return failed_api_response(ErrorCode.REFUSE_ACCESS, "Can not delete interpretation of other users!")

    this_interpretation.delete()

    ret = {}
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('PUT')
def changeInterpretation(request: HttpRequest, id: int):
    # print('[DEBUG] Got request for change interpretation.')
    assert request.body.decode() != '{}'

    data: dict = parse_data(request)
    user = request.user

    content: str = data.get('content')
    title: str = data.get('title')
    # tags: list = data.get('tags')
    source: str = data.get('source')
    citation: str = data.get('citation')
    publish_year: int = data.get('published_year')

    this_interpretation = Interpretation.objects.get(pk=id)
    
    # identity check
    if user != this_interpretation.created_by:
        return failed_api_response(ErrorCode.REFUSE_ACCESS, "Can not delete interpretation of other users!")

    this_interpretation.content = content
    this_interpretation.title = title
    # this_interpretation.tags = tags
    this_interpretation.source = source
    this_interpretation.citation = citation
    this_interpretation.publish_year = publish_year

    this_interpretation.save()

    # print('[DEBUG] Changed interpretation.')
    ret = {}
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def getInterpretation(request: HttpRequest, id: int):
    # _created_by = {
    #     'id': 234,
    #     'username': 'JacquesdeH',
    #     'institution': 'Beihang University',
    # }  # TODO: hash type?
    # _tags = [
    #     'Deep Learning',
    #     'Few-Shot Learning'
    # ]  # TODO: hash type?

    # ret = {
    #     'id': 233,  # main key of interpretation
    #     'created_by': _created_by,
    #     'content': '这是一个很优秀的论文解读，牛逼！',
    #     'citation': '解读对象 Attention is all you need.',
    #     'source': 'https://arxiv.org/pdf/2102.04095.pdf',
    #     'publish_year': datetime.strptime('2021 04 21 11:17:26 848749'),
    #     'title': 'Attention is allllll you need!!',
    #     'tags': _tags,
    # }

    # ret = {
    #     'title': 'Attention is all you need!',
    #     'content': '这是一个很优秀的论文解读content，牛逼！',
    #     'favor_num': 2334,
    #     'like_num': 123445,
    #     'id': 999,
    # }

    user = request.user
    this_interpretation = Interpretation.objects.get(pk=id)

    # update viscount
    this_interpretation.viscount += 1
    this_interpretation.save()

    ret = dict()

    ret.update(this_interpretation.to_hash(current_user=user))
    # import pdb
    # pdb.set_trace()
    return success_api_response(ret)


# @response_wrapper
# @jwt_auth()
@require_http_methods('GET')
def downloadInterpretation(request: HttpRequest, id: int):
    print('[DEBUG] Downloading process called.')
    user = request.user
    this_interpretation = Interpretation.objects.get(pk=id)
    this_content = this_interpretation.content
    this_title = this_interpretation.title
    if not os.path.exists(PDF_CACHE_DIR):
        os.mkdir(PDF_CACHE_DIR)
    this_pdf_name = f'{this_title}.pdf'
    this_pdf_path = os.path.join(PDF_CACHE_DIR, this_pdf_name)
    pdfkit.from_string(input=this_content.encode().decode('utf-8'), output_path=this_pdf_path)

    response = FileResponse(open(this_pdf_path, 'rb'), filename=this_pdf_name, as_attachment=True)
    response['Content-Type'] = 'application/octet-stream'
    print('[DEBUG] Right before returning response of file download.')
    return response


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def collectInterpretation(request: HttpRequest, eid: int):
    user = request.user
    this_interpretation = Interpretation.objects.get(pk=eid)

    this_interpretation.collectors.add(user)

    this_interpretation.save()

    ret = {}
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def uncollectInterpretation(request: HttpRequest, eid: int):
    user = request.user
    this_interpretation = Interpretation.objects.get(pk=eid)

    this_interpretation.collectors.remove(user)

    this_interpretation.save()

    ret = {}
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def likeInterpretation(request: HttpRequest, id: int):
    # data: dict = parse_data(request)
    user = request.user

    this_interpretation = Interpretation.objects.get(pk=id)

    current_status = user in this_interpretation.likers.all()

    # revert like status
    if current_status == True:
        this_interpretation.likers.remove(user)
    else:
        this_interpretation.likers.add(user)
        Notification.new_notification(
            code=PAP_COMMENT_LIKE,
            from_user=user,
            to_user=this_interpretation.created_by,
            content="Liked an interpretation",
            pap_model=this_interpretation
        )
    
    this_interpretation.save()

    ret = {}
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('POST')
def transmitInterpretation(request: HttpRequest, id: int):
    user = request.user

    this_interpretation = Interpretation.objects.get(pk=id)

    this_interpretation.forwarders.add(user)

    this_interpretation.save()

    ret = {}
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def recommendInterpretation(request: HttpRequest):
    NUM_RECOMMEND = 10

    interpretations = Interpretation.objects
    # filter out by current user
    # interpretations = interpretations.filter(~Q(created_by__pk=request.user.pk))
    # sort with viscount with highest first
    interpretations = interpretations.order_by('-viscount')

    ret = [_inter.to_hash() for _inter in interpretations.all()[:min(NUM_RECOMMEND, len(interpretations))]]
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def randomWalkInterpretation(request: HttpRequest):
    NUM_SELECT = 10

    interpretations = Interpretation.objects
    interpretations = interpretations.filter(~Q(created_by__pk=request.user.pk))
    interpretations = interpretations.distinct()
    interpretations = [_inter for _inter in interpretations.all()]
    _num_select = min(NUM_SELECT, len(interpretations))
    interpretations = random.sample(population=interpretations, k=_num_select)
    random.shuffle(interpretations)

    ret = [_inter.to_hash() for _inter in interpretations]
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def searchInterpretation(request: HttpRequest, pid: int):
    ITEM_PER_PAGE = 5
    
    # import pdb
    # pdb.set_trace()
    data = request.GET.dict()
    user = request.user

    keyword: str = data.get('keywords')
    author: str = data.get('author')
    
    # update keyword database
    print(keyword)
    _keyword_matches = Keyword.objects.filter(name=keyword.lower())
    if _keyword_matches.count() == 0:
        this_keyword = Keyword(name=keyword.lower())
        this_keyword.count += 1
        this_keyword.save()
    else:
        assert _keyword_matches.count() == 1, "Wrong keyword set occurred !"
        this_keyword = _keyword_matches.all()[0]
        this_keyword.count += 1
        this_keyword.save()
    # import pdb
    # pdb.set_trace()

    _query_content = Q(content__icontains=keyword)
    _query_title = Q(title__icontains=keyword)
    _keyword_matches = Interpretation.objects.filter(_query_content | _query_title).all()
    if (author is None) or (author == ''): 
        _all_matches = _keyword_matches
    else:
        _all_matches = _keyword_matches.filter(created_by__username=author)
    
    ret = [_interpretation.to_hash(current_user=user) for _interpretation in _all_matches]

    # select this page for return
    item_L = ITEM_PER_PAGE * (pid - 1)
    item_R = min(ITEM_PER_PAGE * (pid), len(ret))

    ret = ret[item_L:item_R]
    print("[DEBUG]")
    print(ret)
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def getAllInterpretation(request: HttpRequest):
    user = request.user
    _all_matches = Interpretation.objects.all()
    ret = [_interpretation.to_hash(current_user=user) for _interpretation in _all_matches]
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def queryVisitorNumber(request: HttpRequest):
    user = request.user
    _all_matches = Interpretation.objects.all()

    cnt = 0
    for _inter in _all_matches:
        cnt += _inter.viscount
    
    ret = {
        'totcount': cnt,
    }

    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def queryKeywordTops(request: HttpRequest):
    TOP_COUNT = 10
    sorted_keywords = Keyword.objects.order_by('-count')
    ret = [_keyword.to_hash() for _keyword in sorted_keywords[:TOP_COUNT]]
    return success_api_response(ret)


@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def queryTagRatio(request: HttpRequest):
    # import pdb
    # pdb.set_trace()
    sorted_tags = sorted(Tag.objects.all(), key=lambda _tag: _tag.interpretations.count(), reverse=True)
    _total_links = 0
    for _tag in sorted_tags:
        _total_links += _tag.interpretations.count()
    ret = [{
        'name': _tag.name,
        'count': _tag.interpretations.count(),
    } for _tag in sorted_tags]

    return success_api_response(ret)


INTERPRETATION_API = wrapped_api({
    'DELETE': deleteInterpretation,
    'PUT': changeInterpretation,
    'GET': getInterpretation,
})

