from django.urls import path
from . import views

urlpatterns = [
    # path('', views.main, name="main"), # 루트 url.py에 작성됨
    # path('posts/', views.post_list, name="post_list"), # 루트 url.py에 작성됨
    path('<int:pk>/', views.post_detail, name="post_detail"),
    path('create/', views.post_create, name="post_create"),
    path('update/<int:pk>/', views.post_update, name="post_update"),
    path('delete/<int:pk>/', views.post_delete, name="post_delete"),
]
