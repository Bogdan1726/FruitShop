from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    objects = None
    created = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='user_messages')

    def __str__(self):
        if self.user is not None:
            return self.user.username
        return 'Шутник'

    class Meta:
        ordering = ('id',)
