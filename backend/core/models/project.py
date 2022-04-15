from django.db import models
from .micro_knowledge import MicroKnowledge
from .user import User

class Project(models.Model):
    create_user = models.ForeignKey(User, related_name='created_project', on_delete=models.CASCADE)
    name = models.CharField(max_length = 100)
    #timeline_list in timeline.py
    content = models.CharField(max_length = 65536)
    html_content = models.CharField(max_length = 65536)
    #discussion_list
    mk_list=models.ManyToManyField(MicroKnowledge,related_name='belonged_project',through='ProjectMicroKnowledge')
    #added_project_mk
    
    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'create_user': self.create_user.simple_to_dict(),
            'name': self.name,
            'content': self.content,
            'html_content': self.html_content,
            'timeline_list': [
                timeline.to_dict() for timeline in self.timeline_list.all()
            ],
        }
    
class ProjectMicroKnowledge(models.Model):
    create_user = models.ForeignKey(User, related_name='added_project_mk', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    micro_knowledge = models.ForeignKey(MicroKnowledge, on_delete = models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_mk_list')
    reason = models.CharField(max_length=5000)
    
    def to_dict(self):
        return {
            'id': self.id,
            'create_user': self.create_user.simple_to_dict(),
            'time': self.time,
            'micro_knowledge_id': self.micro_knowledge.id,
            'reason': self.reason,
        }
    