from django.contrib import admin
from .models import Post, Comment, Like, Tag, Promotion

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Promotion)