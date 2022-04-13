import copy
import json
import random
import numpy as np
from django.http import HttpRequest
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from django.db.models import Count
from core.models.user import User
from core.models.tag import Tag
from core.api.utils import response_wrapper, success_api_response, failed_api_response, ErrorCode
from core.api.auth import jwt_auth
from core.api.query_utils import query_page

@response_wrapper
@jwt_auth()
@require_GET
@query_page()
def recommend(request: HttpRequest, *args, **kwargs):
    """recommend

    Arguments:
        request {HttpRequest} -- get

    Params:
        page
        page_size
        num

    Returns:
        dict -- recommend
    """
    data = request.GET.dict()
    num = int(data.get('num'))
    query_type = data.get('type', None)
    res = get_recommend(request.user.id, num)
    if query_type == '1':
        models = MicroEvidence\
            .search_by_keywords_and_tags(keywords=data.get('keywords', None), tags=data.get('tags', None))\
            .filter(pk__in=res)
    if query_type == '0':
        models = MicroConjecture\
            .search_by_keywords_and_tags(keywords=data.get('keywords', None), tags=data.get('tags', None))\
            .filter(pk__in=res)
    else:
        models = MicroKnowledge\
            .search_by_keywords_and_tags(keywords=data.get('keywords', None), tags=data.get('tags', None))\
            .filter(pk__in=res)
    models_all = models.count()
    page = kwargs.get('page')
    page_size = kwargs.get('page_size')
    paginator = Paginator(models, page_size)
    page_all = paginator.num_pages

    if page > page_all:
        models_info = []
    else:
        models_info: list = []
        for item in models:
            tag_list: list = []
            for tag in item.tag_list.all():
                tag_list.append({
                    "name": tag.name,
                    "type": tag.type
                })
            published_year = None
            source = None
            citation = None
            microevidence = MicroEvidence.objects.filter(pk=item.id).exists()
            microconjecture = not microevidence
            if microevidence:
                me = MicroEvidence.objects.get(pk=item.id)
                published_year = me.published_year
                source = me.source
                citation = me.citation
            models_info.append({
                'id': item.id,
                'created_at': item.created_at,
                'content': item.content,
                'judge_status': item.judge_status,
                'microconjecture': microconjecture,
                'microevidence': microevidence,
                'tag_list': tag_list,
                'created_by__id': item.created_by.id,
                'created_by__nick_name': item.created_by.nick_name,
                'created_by__username': item.created_by.username,
                'published_year': published_year,
                'source': source,
                'citation': citation,

                'like_num': item.like_list.all().count(),
                'favor_num': item.favorites.all().count(),

                'is_like': item.like_list.filter(id=request.user.id).exists(),
                'is_favor': request.user.favorites.filter(id=item.id).exists()
            })
        paginator = Paginator(models_info, page_size)
        models_info = list(paginator.get_page(page))
    data = {
        'models_all': models_all,
        'total_count': paginator.count,
        'page_all': page_all,
        'page_now': page,
        'models': models_info
    }
    return success_api_response(data)

# @jwt_auth()
def get_recommend(user_id: int, num: int):
    """recommend

    Arguments:
        user_id {int} -- user id
        num {int} -- recomment num

    Returns:
        dict -- recommend result
    """
    user_all = User.objects.all()
    data: dict = {}
    for user in user_all:
        tags = user.user_tags[1:-1]
        tag_favor: list = [0]*70 if tags == '' else [int(s) for s in tags.split(',')]
        user_favor = user.favorites.all()
        micro_knowledge = list(user_favor.values_list('id', flat=True)) if user_favor else []
        data[user.id] = {
            'tag_favor': tag_favor,
            'micro_knowledge': micro_knowledge
        }
    user = copy.deepcopy(data)
    r = Recommender(user, k=5, n=num)
    res = r.recommend(user_id)
    return res


class Recommender:
    '''
    users：用户集
    k：表示得出最相近的k的近邻
    n：表示需要推荐的物品数，如不够则随机从微知识库里挑选一些
    '''
    def __init__(self, users, k=3, n=10):
        self.k = k
        self.n = n
        self.users = users
        # 对 user 的标签向量进行归一化
        for instance in self.users:
            self.users[instance]['tag_favor'] = self.normalize(self.users[instance]['tag_favor'])

    def normalize(self, x):
        '''
        将标签向量归一化，使得各分量之和为1，以避免造成新用户由于缺乏偏好数据本身标签向量就要比老用户小
        hope this work!
        '''
        total = np.sum(x) if np.sum(x) else 1
        x = np.array(x) / total
        return x

    def euclideanDistence(self, x, y):
        '''
        用于计算标签向量之间的距离
        x, y：标签向量
        '''
        return np.linalg.norm(x-y)
        
    def compute_nearest_neighbor(self, username):
        distances = []
        for instance in self.users:
            if instance != username:
                distance = self.euclideanDistence(self.users[username]['tag_favor'], self.users[instance]['tag_favor'])
                distances.append((instance, distance))

        distances.sort(key=lambda tuple: tuple[1])
        return distances
    
    #推荐算法的主体函数
    def recommend(self, username):
        '''
        实际的时候，可以直接使用 id
        '''
        #存储微知识id以及对应的权重，设成字典是为了方便下面的加权重
        recommendations = {}
        #计算出user与所有其他用户的相似度，返回一个list
        nearest = self.compute_nearest_neighbor(username)
        # print nearest
        print('nearest: ', nearest)
        user_favor = self.users[username]['micro_knowledge']
        # print userRatings
        total_distance = 0.0
        #得住最近的k个近邻的总距离
        for i in range(min(self.k, len(nearest))):
            total_distance += nearest[i][1]
        if total_distance == 0.0:
            total_distance = 1.0
            
        #将与user最相近的k个人中user没有看过的书推荐给user，并且这里又做了一个分数的计算排名
        for i in range(min(self.k, len(nearest))):
        #第i个人的与user的相似度，转换到[0,1]之间
        #这个weight算得过于草率
            weight = 1 - nearest[i][1] / total_distance
        
        #第i个人的name
            name = nearest[i][0]
        
        #第i个用户的发布或者收藏
            neighbor_favor = self.users[name]['micro_knowledge']
        
            for knowledge in neighbor_favor:
                if knowledge not in user_favor:
                    if knowledge not in recommendations:
                        recommendations[knowledge] = weight # 这里的权重当前仅考虑了当前用户与邻居的相似度，之后还可以考虑 knowledge 自身的点赞数、收藏数等
                    else:
                        recommendations[knowledge] = (recommendations[knowledge]+ weight)
            
        recommendations = list(recommendations.items()) # 转化成 (id, weight) tuple 的数组
        
        #做了一个排序
        recommendations.sort(key=lambda tuple: tuple[1], reverse=True)
        recommendations = list(map(lambda tuple: tuple[0], recommendations))
        # 若推荐数目不足 n，则进行填充
        if len(recommendations) < self.n:
        # 随机选一些微知识进行填充，如果可以的话，可以按照用户的标签向量作为依据，进行选取
        # 这里将使用随机数进行模拟
            tags_id = self.users[username]['tag_favor']
            tags_id = tags_id.tolist()
            max_index = tags_id.index(max(tags_id))
            mk = list(MicroKnowledge.objects.filter(judge_status=1).values_list('id', flat=True))
            if max_index != 0:
                tag = Tag.objects.get(id=max_index)
                mk = list(tag.tag_to_mk.filter(judge_status=1).values_list('id', flat=True)) if tag.tag_to_mk.all() else mk
            x = self.n - len(recommendations)
            if x < len(mk):
                random_list = np.random.choice(mk, x, replace=False).tolist()
                for item in random_list:
                    recommendations.append(item)
            else:
                for item in mk:
                    recommendations.append(item)
        return recommendations