from django.db import models
from .user import User

VERIFY_TYPE_CHOICES = (
    (0, 'Unverified'),
    (1, 'Verified'),
    (2, 'Failed'),
)


class VerifyUser(models.Model):
    """comment

    Fields:
        - user: a foreignkey to User
        - created_at = created time
        - description: company's descriotion of the demand
        - title: title of the demand
        - meta: other informatino about the demand
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sended_demands")
    meta = models.CharField(max_length=1000)
    verified_type = models.IntegerField(choices=VERIFY_TYPE_CHOICES,default= 0)

    def set_verified(self):
        """
        把认证状态标注为通过
        :return: 操作是否成功: boolean
        """
        try:
            self.verified_type = 1
            self.save()
            # print("[DBEUG] message already read"+ self.read_state)
            return True
        except Exception:
            return False

    def set_failed(self):
        """
        把认证状态标注为失败
        :return: 操作是否成功: boolean
        """
        try:
            self.verified_type = 2
            self.save()
            # print("[DBEUG] message already read"+ self.read_state)
            return True
        except Exception:
            return False


