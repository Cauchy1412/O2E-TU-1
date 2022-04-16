from django.db import models

from .pap_model import PapModel
from core.models.user import User

UNREAD = 0
READ = 1

READ_STATUS_CHOICES = (
    (UNREAD, 'unread'),
    (READ, 'read'),
)

PAP_COMMENT_FAVOR = 1
PAP_COMMENT_LIKE = 2
PAP_COMMENT_FORWARD = 3
PAP_COMMENT_REPLY = 4
USER_FOLLOW = 5
PAP_COMMENT_RELEASE = 6


CODE_CHOICE = (
    (PAP_COMMENT_FAVOR, "Your paper comment has been favored."),
    (PAP_COMMENT_LIKE, "Your paper comment has been liked."),
    (PAP_COMMENT_FORWARD, "Your paper comment has been forwarded"),
    (PAP_COMMENT_REPLY, "Your paper comment has been replied to"),
    (USER_FOLLOW, "You have been followed."),
    (PAP_COMMENT_RELEASE, "Your following users have released new comments.")
)


class Notification(models.Model):
    """ notification

    Fields:
        - content: notification content
        - read_status: status of notification
    """
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1000)
    read_status = models.IntegerField(choices=READ_STATUS_CHOICES)
    code = models.IntegerField(choices=CODE_CHOICE)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='to_user')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='from_user')
    pap_model = models.ForeignKey(PapModel, on_delete=models.CASCADE, blank=True, null=True)

    def to_hash(self):
        rst = dict()
        rst.update({
            'created_at': self.created_at,
            'from_user': self.from_user.pk,
            'to_user': self.to_user.pk,
            'content': self.content,
            'code': self.code,
            'read_status': self.read_status
        })
        if self.pap_model is not None:
            rst.update({
                'pap_model': self.pap_model.pk
            })
        return rst

    def has_read(self):
        self.read_status = READ
        self.save()

    @classmethod
    def new_notification(cls,
                         code: int,
                         from_user: User,
                         to_user: User,
                         content: str,
                         pap_model=None):
        try:
            new_notification = Notification(code=code,
                                            content=content,
                                            from_user=from_user,
                                            to_user=to_user,
                                            read_status=UNREAD)
            if pap_model is not None:
                new_notification.pap_model = pap_model
            new_notification.save()
            return True
        except Exception:
            return False
