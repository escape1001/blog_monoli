from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('mypage/', views.mypage, name="mypage"),
    # path('profile/<str:username>', views.profile, name="mypage"),
]
