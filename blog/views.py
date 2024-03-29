from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Post, Comment, Tag, Like, Promotion
from accounts.models import Profile
from blog.forms import CommentForm
from django.db.models import Q
from django.db.models import F, Count
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404



class Main(ListView):
    model = Post
    template_name = 'blog/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 프로모션 리스트화
        promotion_list = Promotion.objects.filter(is_show=True)
        # 최신 글 상위 6개
        latest_list = Post.objects.all().order_by('-created_at')[:6]
        # 인기글 상위 6개
        popular_list = Post.objects.annotate(
            total_popularity=F('view_count') + Count('comments')*2.5 + Count('likes')*2
        ).order_by('-total_popularity')[:6]

        context['promotion_list'] = promotion_list
        context['latest_list'] = latest_list
        context['popular_list'] = popular_list
        
        return context


class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_queryset(self):
        queryset = super().get_queryset()

        q = self.request.GET.get('q', '')
        tags = self.request.GET.getlist('tag')

        if q :
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(contents__icontains=q)
            ).distinct()

        for tag in tags:
            if tag:
                queryset = queryset.filter(
                    tags__name__iexact=tag
                )

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags'] = tags
        
        return context


class PostDetail(DetailView):
    model = Post

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=pk)
        post.view_count += 1
        post.save()
        return super().get_object(queryset)
    
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        
        current_post = self.object
        prev_post = Post.objects.filter(pk__lt=current_post.pk).order_by('-pk').first()
        next_post = Post.objects.filter(pk__gt=current_post.pk).order_by('-pk').first()
        
        try:
            author_info = Profile.objects.get(user=current_post.author)
            context['author_info'] = author_info
        except Profile.DoesNotExist:
            pass
        
        try :
            liked = bool(Like.objects.filter(post=current_post, author=user))
            context['liked'] = liked
        except:
            pass

        context['prev_post'] = prev_post
        context['next_post'] = next_post
        
        return context
    
    @method_decorator(login_required)
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

    def form_valid(self, form):
        video = form.save(commit=False)
        video.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('post_detail', args=[str(self.object.pk)])


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


class CommentUpdate(UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['contents']

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('post_detail', args=[str(self.object.post.pk)])
    

class CommentDelete(UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('post_detail', args=[str(self.object.post.pk)])
    

class LikeToggle(LoginRequiredMixin, View):
    model = Like
    
    def post(self, request, *args, **kwargs):  
        post_pk = kwargs.get('pk')
        author = request.user

        try:
            like_obj = Like.objects.get(post_id=post_pk, author=author)
            like_obj.delete()
        except Like.DoesNotExist:
            like_obj = Like.objects.create(post_id=post_pk, author=author)
            like_obj.save()

        return HttpResponseRedirect(reverse('post_detail', args=[str(post_pk)]))



main = Main.as_view()
post_list = PostList.as_view()
post_detail = PostDetail.as_view()
post_create = PostCreate.as_view()
post_update = PostUpdate.as_view()
post_delete = PostDelete.as_view()
comment_update = CommentUpdate.as_view()
comment_delete = CommentDelete.as_view()
post_like = LikeToggle.as_view()