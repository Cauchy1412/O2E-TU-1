"""
message: 文字消息
"""
from django.db import models
from django.contrib.auth import get_user_model
from .user import User

UNREAD = 0
READ = 1

READ_STATE_CHIOCES = (
    (0, 'Not read'),
    (1, 'Read'),
)

class Message(models.Model):
    """
    Field:
        - content
        - from_user
        - to_user
        - created_at
    """
    content = models.CharField(max_length=140)
    from_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_sender")
    to_user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="chat_receiver")
    created_at = models.DateTimeField(auto_now_add=True)
    read_state = models.IntegerField(choices=READ_STATE_CHIOCES)

    def set_read(self):
        """
        把消息标注为已读
        :return: 操作是否成功: boolean
        """
        try:
            self.read_state = READ
            self.save()
            print("[DBEUG] message already read"+ self.read_state)
            return True
        except Exception:
            return False

    def to_hash(self):
        rst = dict()
        rst.update({
            'id': self.id,
            'content':self.content,
            'from_user': self.from_user,
            'to_user': self.to_user,
            'created_at': self.created_at,
        })
        return rst

    def to_dict(self):
        return {
            'message_id' : self.id,
            'from_user_id': self.from_user.id,
            'to_user_id': self.to_user.id,
            'from_user_name': self.from_user.username,
            'to_user_name': self.to_user.username,
            'from_user_pic': self.from_user.get_icon(),
            'to_user_pic': self.to_user.get_icon(),
            'created_at': self.created_at,
            'read_state': self.read_state,
            'content': self.content
        }


    @classmethod
    def new_message(cls,
                         from_user: User,
                         to_user: User,
                         content: str):
        try:
            new_message = Message(content=content,
                                from_user=from_user,
                                to_user=to_user,
                                read_state=UNREAD)
        #print("[DEBUG] message:"+ new_message.to_dict())
            new_message.save()
            return new_message.id
        except Exception:
            return -1
