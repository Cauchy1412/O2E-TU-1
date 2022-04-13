"""tag model
"""
from django.db import models

TAG = 0
KEYWORD = 1

TAG_TYPE_CHOICES = (
    (TAG, 'Tag'),
    (KEYWORD, 'Keyword'),
)


class Tag(models.Model):
    """tag

    Fields:
        - name: tag's name
        - type: it's a tag or keyword
    """
    name = models.CharField(max_length=30)
    type = models.IntegerField(choices=TAG_TYPE_CHOICES)

    def to_hash(self):
        rst = dict()
        rst.update({
            "id": self.id,
            "name": self.name,
            "type": self.type,
        })
        return rst