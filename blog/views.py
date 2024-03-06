from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Comment, Tag
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class Main(ListView):
    pass

class PostList(ListView):
    pass

class PostDetail(DetailView):
    pass

class PostCreate(CreateView):
    pass

class PostUpdate(UpdateView):
    pass

class PostDelete(DeleteView):
    pass

main = Main.as_view()
post_list = PostList.as_view()
post_detail = PostDetail.as_view()
post_create = PostCreate.as_view()
post_update = PostUpdate.as_view()
post_delete = PostDelete.as_view()