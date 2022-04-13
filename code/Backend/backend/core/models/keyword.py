from django.db import models
from django.db.models.fields import CharField, IntegerField


class Keyword(models.Model):

    name = CharField(primary_key=True, max_length=30)
    count = IntegerField(default=0)

    def to_hash(self):
        return {
            'name': self.name,
            'count': self.count,
        }