from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from blog.models import Post, Comment, Like
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q



signup = CreateView.as_view(
    form_class = UserCreationForm,
    template_name = "accounts/accounts_form.html",
    success_url = settings.LOGIN_URL
)

login = LoginView.as_view(
    template_name = "accounts/accounts_form.html",
)

logout = LogoutView.as_view(
    next_page=settings.LOGIN_REDIRECT_URL,
)


def profile(request, username):
    user_obj = User.objects.get(username=username)
    posts = Post.objects.filter(author=user_obj)

    context = {
        "posts" : posts,
        "author" : user_obj,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def mypage(request):
    comments = Comment.objects.filter(author=request.user)
    liked = Like.objects.filter(author=request.user).values_list('post', flat=True)
    liked_posts = Post.objects.filter(pk__in=liked)
    commented_my = Post.objects.filter(author=request.user).annotate(num_comments=Count('comments')).filter(num_comments__gt=0)
    commented_myposts = Comment.objects.filter(~Q(author=request.user), post__in=commented_my)

    context = {
        "comments" : comments,
        "liked_posts" : liked_posts,
        "commented_myposts" : commented_myposts,
    }

    return render(request, 'accounts/mypage.html', context)