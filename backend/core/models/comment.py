"""comment
"""
from django.db import models
from .user import User
# from .micro_knowledge import MicroKnowledge
from .user import User
from .tag import Tag
from .interpretation import Interpretation

class Comment(models.Model):
    """comment

    Fields:
        - interpretation: a foreignkey to interpretation
        - user: a foreignkey to User
        - created_at = created time
        - text: comment content
    """
    interpretation = models.ForeignKey(Interpretation, on_delete=models.CASCADE, related_name="comment_list")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sended_comments")
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=200)
    to_user = models.ForeignKey(User, on_delete=models.PROTECT, null = True, related_name="recived_comments")
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name="son_comment")

