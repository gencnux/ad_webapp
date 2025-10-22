from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CommandLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    command_id = models.CharField(max_length=100)
    parameters = models.TextField()
    output = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.command_id} - {self.timestamp}"