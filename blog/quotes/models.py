from django.db import models

from users.models import User


class Quote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    added_by = models.ForeignKey(User)
    contents = models.TextField()
    author = models.TextField()