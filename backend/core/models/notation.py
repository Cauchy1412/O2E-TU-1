"""
    notation
"""
from django.db import models
from .tag import Tag
from .user import User
from .pap_model import PapModel,NOTATION

class Notation(PapModel):

    
    def to_hash(self) -> dict:
        # TODO
        rst = dict()
        return rst
        

    def pap_type(self):
        return NOTATION


