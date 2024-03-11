from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from blog.models import Post, Comment, Like
from accounts.models import Profile
from django.contrib.auth.models import User
from django.db.models import Count
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth import login as auth_login



class Signup(CreateView):
    form_class = UserCreationForm
    template_name = "accounts/accounts_form.html"

    def form_valid(self, form): # 회원가입 시 자동 로그인하고 프로필페이지로 리디렉
        user = form.save()
        auth_login(self.request, user)

        return redirect("/accounts/mypage")

signup = Signup.as_view()

login = LoginView.as_view(
    template_name = "accounts/accounts_form.html",
)

logout = LogoutView.as_view(
    next_page=settings.LOGIN_REDIRECT_URL,
)


def userhome(request, username):
    user_obj = User.objects.get(username=username)
    profile = Profile.objects.get(user=user_obj)
    posts = Post.objects.filter(author=user_obj)

    context = {
        "posts" : posts,
        "profile" : profile,
        "author" : user_obj,
    }

    return render(request, 'accounts/userhome.html', context)


@login_required
def mypage(request):
    profile = Profile.objects.get(user=request.user)
    comments = Comment.objects.filter(author=request.user)
    liked = Like.objects.filter(author=request.user).values_list('post', flat=True)
    liked_posts = Post.objects.filter(pk__in=liked)
    commented_my = Post.objects.filter(author=request.user).annotate(num_comments=Count('comments')).filter(num_comments__gt=0)
    commented_myposts = Comment.objects.filter(~Q(author=request.user), post__in=commented_my)

    context = {
        "profile" : profile,
        "comments" : comments,
        "liked_posts" : liked_posts,
        "commented_myposts" : commented_myposts,
    }

    return render(request, 'accounts/mypage.html', context)