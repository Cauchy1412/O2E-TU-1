"""
Chatroom: 聊天室，目前只支持两人
"""

from django.db import models

from .message import Message
from .user import User


class Chatroom(models.Model):

    """
    Fields:
        - id
        - owner: owner of the chatroom
        × user_list: a list of Users(later)
        - created_at: the time of last message
        - message: list of messages

    """
    name = models.CharField(max_length=30, default="chat")
    owner = models.ForeignKey('User', on_delete=models.CASCADE, related_name= "chatroom_list")
    #created_at = models.DateTimeField(auto_now_add=True)
    message = models.ManyToManyField('Message', related_name='message_list')
    #TODO: change the mode to CASCADE, but may have problems.
    to_user = models.ForeignKey('User', on_delete=models.CASCADE, null=True,
                                related_name="joined_chatroom_list")
    demand = models.ForeignKey('Demand', on_delete=models.CASCADE, null=True, related_name= "demand_rooms")


    # parent_chatroom = models.ForeignKey('Chatroom',
    #                                       on_delete=models.CASCADE, null=True,
    #                                       related_name="son_chatroom")


    def to_dict(self) -> dict:
        rst = dict()
        rst.update(
            {'chatroom_id': self.id,
             'from_user_id': self.owner.pk,
             'to_user_id': self.to_user.pk,
             'from_user_name': self.owner.username,
             'to_user_name' : self.to_user.username,
             'from_user_pic': self.owner.get_icon(),
             'to_user_pic': self.to_user.get_icon(),
             'demand_id' : self.demand and self.demand.id,
             #'created_at': self.created_at,
             'message_list': [mess.to_dict() for mess in self.message.all()]
             }
        )
        # if self.parent_chatroom is not None:
        #     data['parent_chatroom_id'] = self.parent_chatroom.id
        return rst

    def add_message(self, mid: int) -> bool:
            """
            add message
            """
            try:
                m = Message.objects.get(id=mid)
                self.message.add(m)
                self.save()
                return True
            except Exception:
                return False
