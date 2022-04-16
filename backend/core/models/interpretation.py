"""
    interpretation
"""

from django.db import models
from .tag import Tag
from .user import User
from .pap_model import PapModel, INTERPRETATION
from backend.settings import DATETIME_FMT

def _safe_content(content: str):
    ret = content
    poisons = ['Alert', 'alert', 'Script', 'script', 'Onerror', 'onerror']
    for _poison in poisons:
        ret = ret.replace(_poison, ' ')
    ERRORMESSAGE = 'The content contains MALICIOUS tokens! Thus NOT displayed.'
    if ret != content:
        return ERRORMESSAGE
    return ret

class Interpretation(PapModel):
    
    citation = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    source = models.URLField()
    publish_year = models.IntegerField()
    tags = models.ManyToManyField(Tag, related_name='interpretations')

    # class Meta:
        # pass

    def to_hash(self, current_user=None):
        rst = dict()

        if current_user is None:
            _is_guanzhu = False
            _is_like = False
            _is_collect = False
        else:
            _is_guanzhu = current_user in self.created_by.followers.all()
            _is_collect = current_user in self.collectors.all()
            _is_like = current_user in self.likers.all()
        _tags = [_tag.to_hash() for _tag in self.tags.all()]
        _created_by = {
            "username": self.created_by.username,
            "id": self.created_by.pk,
        }

        #根据输入的论文解读 id 输出如下
        data = {
            "isguanzhu": _is_guanzhu,
            "title": self.title,
            "id": self.pk,  #论文解读id
            "is_like": _is_like,
            "is_favor": _is_collect,
            "commentNum": self.comment_list.count(),  #论文解读评论数量
            "created_at": self.created_at.strftime(DATETIME_FMT),  #创建时间
            "like_num": self.likers.count(),
            'favor_num': self.collectors.count(),
            "tags": _tags,  #标签
            "content": _safe_content(self.content),  #论文解读全部内容
            "uid": self.created_by.id,  #用户ID
            "userpic": self.created_by.icon.url,  #用户头像
            "created_by": _created_by,
            "source": self.source,
            "citation": self.citation,
            "published_year": self.publish_year,
            "viscount": self.viscount,
        }

        # import pdb
        # pdb.set_trace()

        rst.update(data)
        return rst
        
    def pap_type(self):
        return INTERPRETATION
    
    def add_tag(self, _tag: Tag):
        # import pdb
        # pdb.set_trace()
        self.tags.add(_tag)
        return True


