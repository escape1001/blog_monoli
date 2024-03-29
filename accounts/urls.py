from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('mypage/', views.mypage, name="mypage"),
    path('update/profile', views.update_profile, name="update_profile"),
    path('update/password', views.update_password, name="update_password"),
    # path('profile/<str:username>', views.profile, name="profile"), # 루트 url.py에 작성됨
]
