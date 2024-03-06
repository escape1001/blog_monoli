from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render
from django.views.generic import CreateView
from blog.models import Post, Comment, Like
from django.contrib.auth.models import User


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
    posts = Post.objects.filter(author=username)
    userinfo = User.objects.get(username=username)
    

    context = {
        "posts" : posts,
        "userinfo" : userinfo,
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def mypage(request):
    posts = Post.objects.filter(author=request.user)
    comments = Comment.objects.filter(author=request.user)
    likes = Like.objects.filter(author=request.user)

    context = {
        "posts" : posts,
        "comments" : comments,
        "likes" : likes,
    }

    return render(request, 'accounts/mypage.html', context)




# path('profile/<str:username>', views.profile, name="mypage"),