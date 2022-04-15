from django.db import models
from .user import User

class Image(models.Model):
    """
        created_at: datetime
        created_by: user
        image: image content
    """
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.ImageField(upload_to="images/%Y%m/%d/images")

    def to_hash(self):
        rst = dict()
        rst.update({
            'id': self.id,
            'file': str(self.file),
            'created_at': self.created_at
        })
        return rst
