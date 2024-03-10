from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView, View
)
from .models import Post, Comment, Tag, Like, Promotion
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class Main(ListView):
    model = Post
    template_name = 'blog/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 프로모션 리스트화
        promotion_list = Promotion.objects.filter(is_show=True)
        # 최신 글 상위 6개
        latest_list = Post.objects.all().order_by('-created_at')[:6]
        # 인기글 상위 6개 (여기서는 댓글 개수로 인기를 판단하도록 예시로 설정)
        popular_list = Post.objects.annotate(num_comments=Count('likes')).order_by('-num_comments')[:6]

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tags = Tag.objects.all()
        context['tags'] = tags
        
        return context

class PostDetail(DetailView):
    model = Post

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        post.view_count += 1
        post.save()
        return super().get_object(queryset)
    
    def get_context_data(self, **kwargs):
        author = self.request.user
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        
        current_post = self.object
        prev_post = Post.objects.filter(pk__lt=current_post.pk).order_by('-pk').first()
        next_post = Post.objects.filter(pk__gt=current_post.pk).order_by('-pk').first()

        try :
            liked = bool(Like.objects.filter(post=current_post, author=author))
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


class CommentUpdate(UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['contents']

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return reverse('post_detail', args=[str(self.object.post.pk)])
    
class CommentDelete(UserPassesTestMixin, DeleteView):
    model = Comment

    def get_success_url(self):
        return reverse('post_detail', args=[str(self.object.post.pk)])

    def test_func(self):
        return self.request.user == self.get_object().author
    

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