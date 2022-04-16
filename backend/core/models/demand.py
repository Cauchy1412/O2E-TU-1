from django.db import models
from .user import User



class Demand(models.Model):
    """comment

    Fields:
        - user: a foreignkey to User
        - created_at = created time
        - description: company's descriotion of the demand
        - title: title of the demand
        - meta: other informatino about the demand
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sended_demands")
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    title = models.CharField(max_length=100)
    meta = models.CharField(max_length=200)

