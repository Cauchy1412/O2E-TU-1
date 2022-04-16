from django.db import models
from django_mysql import JSONField
from .user import User



class Demand(models.Model):
    """comment

    Fields:
        - interpretation: a foreignkey to interpretation
        - user: a foreignkey to User
        - created_at = created time
        - text: comment content
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sended_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)
    others = JSONField()

