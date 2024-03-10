from django.db import models
from django.contrib.auth.models import User

def get_default_nickname():
    return User.username

class Profile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=10, default=get_default_nickname)
    profile_image = models.ImageField(
        upload_to="profile/%Y/%m/%d/", blank=True
    )

    def __str__(self):
        return self.nickname