from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.utils import timezone
from django.core import serializers


from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

@jwt_auth()
@require_GET
@response_wrapper
def get_papComment(request: HttpRequest, id: int):
    #输入id为论文解读的id，输出该论文解读的所有评论
    #评论只会有两层结构
    ret=[{
    "content": "这里水很深", # 评论内容
    "createTime": "2021-04-28T07:27:28.000+00:00",
    "id": 1, # 评论id
    "parentId":None,
    "uid": 4,#用户id
    "tid": 1,#论文解读id
    "username": "小潘",
    "userpic": "https://pic2.zhimg.com/80/v2-cec0bd850ad3296aa63b4aaa946d3571_1440w.jpg",
    "children":[{
        "content": "什么意思", # 评论内容
        "createTime": "2021-04-28T07:28:28.000+00:00",
        "id": 3, # 评论id
        "parentId":1,
        "uid": 4,
        "tid": 1,#论文解读id
        "username": "frank909",
        "userpic": "http://114.115.168.211:8000/api/images/202104/27/icons/16195110527980.png",
        "children":None
    }]
    },{
    "content": "写的真好", # 评论内容
    "createTime": "2021-04-28T07:28:28.000+00:00",
    "id": 2, # 评论id
    "parentId":None,
    "uid": 4,
    "tid": 1,#论文解读id
    "username": "小嘎",
    "userpic": "https://pic2.zhimg.com/80/v2-eb9500b12175f833d0944bbd19cad079_1440w.jpg",
    "children":None
    },]
    return success_api_response(ret)


@jwt_auth()
@require_POST
@response_wrapper
def delete_papComment(request: HttpRequest,id):
    #输入id是要删除评论的id
    ret={}
    return success_api_response(ret)


@jwt_auth()
@require_POST
@response_wrapper
def create_papComment(request: HttpRequest):
    data: dict = parse_data(request)
    uid = data.get("uid") #评论用户
    parentId = data.get("parentId") 
    #parent Id:评论继承其他评论的id，null表示没有,如果parent评论还有父亲则一直找到没有父亲的parentId
    #即参考知乎的只有两层结构的评论
    id = data.get("id") #论文解读id
    content = data.get("content") #评论内容
    print(data)
    ret={

    }
    return success_api_response(ret)