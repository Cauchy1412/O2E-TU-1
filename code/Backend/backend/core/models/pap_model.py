"""paper model
"""
from django.db import models
from .tag import Tag
from .user import User

PAP_COMMENT = 0
INTERPRETATION = 1
NOTATION = 2


class PapModel(models.Model):
    """Pap model

    Fields:
    // to be finished
        - created_at: created time
        - created_by: A foreignkey to user
    """

    viscount = models.IntegerField(default=0)
    content = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_by')
    likers = models.ManyToManyField(User, related_name='like_list')
    forwarders = models.ManyToManyField(User, related_name='forward_list')
    collectors = models.ManyToManyField(User, related_name='collect_list')

    # class Meta:
        # abstract = True
        # pass

    def pap_type(self):
        return PAP_COMMENT

    def like_num(self):
        return self.likers.values().count()

    def collect_num(self):
        return self.collectors.values().count()

    
