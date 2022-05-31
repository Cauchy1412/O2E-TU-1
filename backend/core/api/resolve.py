"""User Management APIs
"""

from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from core.models import resolution

from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response, wrapped_api)
from core.api.send_email import make_confirm_string, send_email, send_forget
from core.models.auth_record import AuthRecord
from core.models.user import User, ConfirmString
from core import logger
from core.models import verify_user, User, Demand
from core.models.resolution import Resolution
from core.models.verify_user import VerifyUser
from django.core.exceptions import ObjectDoesNotExist
from core.api.ContrastiveSciBERT import ContrastiveSciBERT
from core.api.milvus import Milvus
import json
import torch
import torch.nn as nn
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModel
import requests
from math import log10

model =  ContrastiveSciBERT(100, 1)
model.load_state_dict(torch.load('/home/xyf/Documents/homework/SoftwareEngineering/recommend/resultModel.pt',map_location='cpu'))
myMilvus = Milvus()
searchPaperUrl = 'http://zhitulist.com/zhitu-data-service/search/paper?id='
searchScholarUrl = 'http://zhitulist.com/zhitu-data-service/search/scholar?id='
score = [7, 3, 1]


@response_wrapper
@jwt_auth()
@require_POST
def recommend(request: HttpRequest):
    """set_verified

    [method]: GET

    [route]: /resolution/recommand

    request: {
		demand_id: int
    }
    """
    data: dict = parse_data(request)
    if not data:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    demand_id = data.get('demand_id')
    demand = Demand.objects.get(id=demand_id)
    keywords = demand.keywords
    keyword = model.get_embeds(keywords)
    keyword = keyword / keyword.norm(dim=1, keepdim=True)
    keyword = keyword.cpu().detach().numpy().tolist()
    ids = myMilvus.milvus_search("O2E", keyword, 10)
    paperIds = []
    scholarIds ={}
    for id in ids[0]:
        res = myMilvus.paper_get_by_id("O2E", id)
        paperIds.append(res[0]['paper_id'])
    for paperId in paperIds:
        response = requests.get(searchPaperUrl + str(paperId))
        result = response.json()
        if result['data']:
            # print(result['data']['scholars'][0:3])
            for i, scholar in enumerate(result['data']['scholars'][0:3]):
                if scholar['scholarId'] not in scholarIds:
                    scholarIds[scholar['scholarId']] = score[i]*(log10(result['data']['ncitation']+1))
                else:
                    scholarIds[scholar['scholarId']] += score[i]*(log10(result['data']['ncitation']+1))
    f = zip(scholarIds.values(), scholarIds.keys())
    f = sorted(f, reverse=True)
    data_list = []
    for scholar in f[0:3]:
        id = scholar[1]
        if User.objects.filter(username=id).exists():
            user = User.objects.get(username=id)
        else:
            response = requests.get(searchScholarUrl + str(id))
            result = response.json()
            username = str(id)
            password = str(id)
            email = str(id)+'@O2E.com'
            user_type = 0
            meta = {
                "name": result['data']['scholarName'],
                "professor": result['data']['fieldSecond'][0] + '之父',
                "gender": result['data']['gender'] if result['data']['gender'] else '男',
                "domains": ",".join(result['data']['fieldSecond']),
                "info": ",".join(result['data']['fieldThird'])
            }
            meta = json.dumps(meta)
            new_user = User.objects.create_user(
                username=username, password=password, email=email, is_confirmed=True, user_type=user_type)
            new_user.save()
            verify_user = VerifyUser(user=new_user, meta=meta)
            verify_user.set_verified()
            verify_user.save()
            user = new_user
        verified_user = user.verified_info.first()
        resolution = Resolution.objects.filter(demand=demand, user=user).first()
        if not resolution:
            resolution = Resolution(demand=demand, user=user) # , meta=verified_user and verified_user.meta)
            resolution.save()
        data = {
            'id': resolution.id,
            'uid': user.id,
            'meta': json.loads(verified_user.meta) if verified_user else {
                'name': 'Sebastian Thrun',
                'professor': '谷歌无人车之父',
                'gender': '男',
                'domains': '人工智能，无人驾驶',
                'info': '我是计算机科学教授，领导着自主视觉小组(AVG)。我的小组是Tübingen大学和位于德国网络谷中心Tübingen的智能系统MPI的一部分。我是Tübingen大学计算机科学系的副系主任，是卓越集群“ML in science”和CRC“Robust Vision”的PI。我也是ELLIS的研究员、董事会成员和ELLIS博士项目的协调员。我的研究小组正在开发用于计算机视觉、自然语言和机器人的机器学习模型，应用于自动驾驶、VR/AR和科学文献分析。'
            }
        }
        data_list.append(data)


    # users = User.objects.filter(user_type=0, verified_info__isnull=False)
    # if users.exists():
    #     users = users[:3]
    # else:
    #     users = User.objects.filter(user_type=0)[:3]

    # data_list = []
    # for user in users:
    #     verified_user = user.verified_info.first()
    #     resolution = Resolution.objects.filter(demand=demand, user=user).first()
    #     if not resolution:
    #         resolution = Resolution(demand=demand, user=user) # , meta=verified_user and verified_user.meta)
    #         resolution.save()
    #     data = {
    #         'id': resolution.id,
    #         'uid': user.id,
    #         'meta': json.loads(verified_user.meta) if verified_user else {
    #             'name': 'Sebastian Thrun',
    #             'title': '谷歌无人车之父',
    #             'sex': '男',
    #             'field': '人工智能，无人驾驶',
    #             'info': '我是计算机科学教授，领导着自主视觉小组(AVG)。我的小组是Tübingen大学和位于德国网络谷中心Tübingen的智能系统MPI的一部分。我是Tübingen大学计算机科学系的副系主任，是卓越集群“ML in science”和CRC“Robust Vision”的PI。我也是ELLIS的研究员、董事会成员和ELLIS博士项目的协调员。我的研究小组正在开发用于计算机视觉、自然语言和机器人的机器学习模型，应用于自动驾驶、VR/AR和科学文献分析。'
    #         }
    #     }
    #     data_list.append(data)
    re_data = {'data_list': data_list}
    return success_api_response(re_data)


def resolution2json(resolution: Resolution) -> dict:
    demand = resolution.demand
    user = demand.user
    verified_user = user.verified_info.first()
    verified_scholar = resolution.user.verified_info.first()
    data = {
        'id' : resolution.id,
        'company_id' : user.id,
        'scholar_id' : resolution.user.id,
        'demand_id' : demand.id,
        'company_meta' : json.loads(verified_user.meta) if verified_user else None,
        'scholar_meta' : json.loads(verified_scholar.meta) if verified_scholar else None,
        'time' : resolution.time,
        'created_at': resolution.created_at,
        'title': demand.title,
        'state' : resolution.state,
        'price' : resolution.price,
    }
    return data

@jwt_auth()
@require_GET
@response_wrapper
def get_resolution(request: HttpRequest, id: int):
    """
    get resolution

    [method]: GET

    [route]: /api/resolution/:id

    parms:
		- id: int
    """
    resolution_id = id
    try:
        resolution = Resolution.objects.get(id=resolution_id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    ret_data = resolution2json(resolution)
    return success_api_response(ret_data)

@jwt_auth()
@require_GET
@response_wrapper
def get_scholar_resolutions(request: HttpRequest):
    """
    get scholar resolutions

    [method]: GET

    [route]: /api/resolution/get-scholar-resolutions

    parms:
    """
    user = request.user
    resolutions = user.received_demands.all()
    ret_resolutions = []
    for resolution in resolutions:
        if resolution.state != 0:
            ret_resolutions.append(resolution)
    ret_data = {'resolution_list': [resolution2json(resolution) for resolution in ret_resolutions]}
    return success_api_response(ret_data)

@jwt_auth()
@require_GET
@response_wrapper
def get_company_resolutions(request: HttpRequest):
    """
    get company resolutions

    [method]: GET

    [route]: /api/resolution/get-company-resolutions

    parms:
    """
    user = request.user
    demands = user.sended_demands.all()
    resolutions = []
    for demand in demands:
        resolutions.extend(demand.resolutions.all())
    ret_resolutions = []
    for resolution in resolutions:
        if resolution.state != 0:
            ret_resolutions.append(resolution)
    ret_data = {'resolution_list': [resolution2json(resolution) for resolution in ret_resolutions]}
    return success_api_response(ret_data)

@response_wrapper
@jwt_auth()
@require_http_methods('GET')
def get_all_orders(request: HttpRequest):
    resolutions = Resolution.objects.all()
    ret_resolutions = []
    for resolution in resolutions:
        if resolution.state != 0:
            ret_resolutions.append(resolution)
    ret_data = {'resolution_list': [resolution2json(resolution) for resolution in ret_resolutions]}
    return success_api_response(ret_data)

@jwt_auth()
@require_POST
@response_wrapper
def update_resolution_state(request: HttpRequest):
    """
    update resolution state

    [method]: POST

    [route]: /api/resolution/update-resolution-state

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
        resolution = Resolution.objects.get(id=id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    if state == 2:
        resolution.set_Accepted()
        d = resolution.demand
        d.state = 1
        d.save()
    elif state == 3:
        d = resolution.demand
        d.state = 2
        d.save()

    resolution.state = state
    resolution.save()
    return success_api_response({'msg': 'Resolution state is updated'})

@jwt_auth()
@require_POST
@response_wrapper
def create_order(request: HttpRequest):
    """
    create order

    [method]: POST

    [route]: /api/resolution/create-order

    parms:
        - id
        - time
        - price
    """
    data: dict = parse_data(request)
    if not data:
        print("print: not data")
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Invalid request args.")
    id = data.get('id')
    time = data.get('time')
    price = data.get('price')
    try:
        resolution = Resolution.objects.get(id=id)
    except ObjectDoesNotExist:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS, "Bad Knowledge ID.")
    resolution.state = 1
    resolution.time = time
    resolution.price = price
    resolution.save()
    return success_api_response({'msg': 'order is created'})
