"""
/                               [blog:main] # 메인페이지
/posts                          [blog:post_list] # 포스트 리스트
/posts?q='keyword'              [blog:post_list] # 해당 키워드가 포함된 title, content가 있는 목록을 가져와야 합니다.
/posts?tag='<str:tag>'          [blog:post_list] # 해당 태그가 달린 목록을 가져와야 합니다.
/post/<int:pk>                  [blog:post_detail] # 포스트 상세보기
/post/create                    [blog:post_form] # 포스트 작성 / 사용자만 접근 가능
/post/update/<int:pk>           [blog:post_form] # 포스트 수정
/post/delete/<int:pk>           [blog:post_delete] # 포스트 삭제
/accounts/signup
/accounts/login
/accounts/logout                # 로그인한 사용자만 접근 가능
/accounts/mypage                # 로그인한 사용자만 접근 가능
/profile/<str:username>         [accounts:profile] # 유저 공개프로필
"""
from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from accounts import views as accounts_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', blog_views.main, name="main"),
    path('posts/', blog_views.post_list, name="post_list"),
    path('post/', include('blog.urls')),
    path('accounts/', include('accounts.urls')),
    path('profile/<str:username>/', accounts_views.profile, name="profile"),
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)