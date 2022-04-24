from django.db import models
from pytz import timezone
from .user import User
from .demand import Demand

RESOLUTION_STATES = (
    (0, 'Unformed'),
    (1, 'Unreceived'),
    (2, 'Accepted'),
    (3, 'Completed'),
    (4, 'Rejected'),
)

class Resolution(models.Model):
    """resolution

    Fields:
        - user: a foreignkey to User
        - demand: a foreignkey to Demand
        - time: begining time of the order
        - state: state of the resolution
        - price: price of the resolution
        - created_at = created time
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_demands")
    demand = models.ForeignKey(Demand, on_delete=models.CASCADE, related_name="resolutions")
    time = models.CharField(max_length=100)
    state = models.IntegerField(choices=RESOLUTION_STATES, default = 0)
    price = models.IntegerField(default = -1)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_Unreceived(self):
        """
        企业下单
        :return: 操作是否成功: boolean
        """
        try:
            self.state = 1
            self.save()
            # print("[DBEUG] message already read"+ self.read_state)
            return True
        except Exception:
            return False

    def set_Accepted(self):
        """
        专家接受订单
        :return: 操作是否成功: boolean
        """
        try:
            self.state = 2
            self.created_at = timezone.now()
            self.save()
            # print("[DBEUG] message already read"+ self.read_state)
            return True
        except Exception:
            return False

    def set_Completed(self):
        """
        企业完成订单
        :return: 操作是否成功: boolean
        """
        try:
            self.state = 3
            self.save()
            # print("[DBEUG] message already read"+ self.read_state)
            return True
        except Exception:
            return False

    def set_Rejected(self):
        """
        企业下单
        :return: 操作是否成功: boolean
        """
        try:
            self.state = 4
            self.save()
            # print("[DBEUG] message already read"+ self.read_state)
            return True
        except Exception:
            return False
