from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post, Comment, Tag
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from .forms import CommentForm


class Main(ListView):
    model = Post
    template_name = 'blog/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 최신 글 상위 6개
        latest_list = Post.objects.all().order_by('-created_at')[:6]

        # 인기글 상위 6개 (여기서는 댓글 개수로 인기를 판단하도록 예시로 설정)
        popular_list = Post.objects.annotate(num_comments=Count('likes')).order_by('-num_comments')[:6]

        context['latest_list'] = latest_list
        context['popular_list'] = popular_list
        
        return context

class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q', '')
        tag = self.request.GET.get('tag', '')

        if q :
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(contents__icontains=q)
            ).distinct()

        if tag :
            queryset = queryset.filter(
                tags__name__iexact=tag
            )

        return queryset

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        
        current_post_pk = self.object.pk
        prev_post = Post.objects.filter(pk__lt=current_post_pk).order_by('-pk').first()
        next_post = Post.objects.filter(pk__gt=current_post_pk).order_by('-pk').first()

        context['prev_post'] = prev_post
        context['next_post'] = next_post
        
        return context
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            author = request.user
            contents = form.cleaned_data["contents"]
            comment = Comment.objects.create(author=author, contents=contents, post=self.object)
            comment.save()
        return super().get(request, *args, **kwargs) 

class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'contents', 'thumbnail_image', 'tags']
    
    def get_success_url(self):
        return reverse('post_detail', args=[str(self.object.pk)])

    def form_valid(self, form):
        video = form.save(commit=False)
        video.author = self.request.user
        return super().form_valid(form)

class PostUpdate(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'contents', 'thumbnail_image', 'tags']

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('post_detail', args=[str(self.object.pk)])

class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')


    def test_func(self):
        return self.request.user == self.get_object().author


main = Main.as_view()
post_list = PostList.as_view()
post_detail = PostDetail.as_view()
post_create = PostCreate.as_view()
post_update = PostUpdate.as_view()
post_delete = PostDelete.as_view()