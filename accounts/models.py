from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)

    def __str__(self):    #To know which user is there
        return self.user.username