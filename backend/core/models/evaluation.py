from django.db import models
from .user import User

class Evaluation(models.Model):
    """comment

    Fields:
        - scholar: a foreignkey to User
        - company: a foreignkey to Company
        - created_at = created time
        - content: content of the evaluation
    """
    scholar = models.ForeignKey(User, on_delete=models.CASCADE, related_name="evaluated_contents")
    company = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sended_contents")
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=500)

