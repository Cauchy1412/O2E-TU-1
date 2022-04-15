from django.db import models
from datetime import datetime

class Timeline(models.Model):
    time = models.DateTimeField()
    event = models.CharField(max_length=100)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='timeline_list')
    
    def to_dict(self):
        return {
            'id': self.id,
            'time': self.time,#.strftime("%Y-%m-%d %H:%M:%S"),
            'event': self.event,
            'project_id': self.project.id,
        }