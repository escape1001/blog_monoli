from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    nickname = models.CharField(max_length=10)
    introduce = models.CharField(max_length=150)
    profile_image = models.ImageField(
        upload_to="profile/%Y/%m/%d/", blank=True
    )

    def __str__(self):
        return self.nickname
    
    def save(self, *args, **kwargs):
        if not self.nickname:
            self.nickname = self.user.username
        if not self.introduce:
            self.introduce = f"안녕하세요! {self.user.username}입니다 :)"

        super().save(*args, **kwargs)
