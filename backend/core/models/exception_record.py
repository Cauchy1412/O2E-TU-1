from django.db import models


class ExceptionRecord(models.Model):
    created_at = models.DateTimeField(auto_new_add=True)
