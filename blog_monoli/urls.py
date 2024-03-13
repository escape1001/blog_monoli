"""
/                               [blog:main] # 메인페이지
posts                          [blog:post_list] # 포스트 리스트 + 검색
posts?q='keyword'              [blog:post_list] # 해당 키워드가 포함된 title, content가 있는 목록을 가져와야 합니다.
posts?tag='<str:tag>'          [blog:post_list] # 해당 태그가 달린 목록을 가져와야 합니다.
post/<int:pk>/                  [blog:post_detail] # 포스트 상세보기
post/create/                    [blog:post_form] # 포스트 작성 / 사용자만 접근 가능
post/update/<int:pk>/           [blog:post_form] # 포스트 수정
post/delete/<int:pk>/           [blog:post_delete] # 포스트 삭제
post/update_comment/<int:pk>/  [blog:comment_update] # 덧글 수정
post/delete_comment/<int:pk>/  [blog:comment_delete] # 덧글 삭제
post/like/<int:pk>/            [blog:post_like] # 좋아요 토글
accounts/signup/
accounts/login/
accounts/logout/                # 로그인한 사용자만 접근 가능
accounts/mypage/                # 로그인한 사용자만 접근 가능
<str:username>/                 [accounts:userhome] # 유저 홈. 해당 사용자의 작성글과 프로필 볼 수 있음
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
    path('<str:username>/', accounts_views.userhome, name="userhome"),
    path('tinymce/', include('tinymce.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)