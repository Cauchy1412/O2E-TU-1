from django.db import models
from .user import User

class Topic(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_post')
    start_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True)
    top = models.BooleanField(default=False)
    # project = models.ForeignKey("Project", on_delete=models.CASCADE, related_name='post_list')
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'created_by': self.created_by.simple_to_dict(),
            'title': self.title,
            'start_time': self.start_time,
            'last_update_time': self.last_update_time,
            'top': self.top,
            'project_id': self.project.id,
            }
