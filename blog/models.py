from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title=models.CharField(max_length=50)
    contents=models.TextField()
    thumbnail_image = models.ImageField(
        upload_to="post/thumbnails/%Y/%m/%d/", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    tags = models.ManyToManyField('Tag', blank=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    

class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    contents = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.contents


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='likes'
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.post} / {self.author}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    

class Promotion(models.Model):
    promo_code = models.CharField(max_length=30)
    q = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    is_show = models.BooleanField(default=False)

    def __str__(self):
        return self.promo_code