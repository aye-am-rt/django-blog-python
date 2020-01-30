from django.urls import path
from .views import (PostListViews, PostDetailViews,
                    PostCreateViews, PostUpdateViews,
                    PostDeleteViews, UserPostListViews)
from . import views

urlpatterns = [
    # path('', views.home, name='blog-home'), this was function based view now below changed
    # to class base listView provided by generic django.
    path('', PostListViews.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListViews.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailViews.as_view(), name='post-detail'),
    path('post/new/', PostCreateViews.as_view(), name='post-create'),
    # new create template will be shared with post update template so django convention
    # is to name it as post_form.html (<name of model>_form.html)
    path('post/<int:pk>/update/', PostUpdateViews.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteViews.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]

# path('', PostListViews.as_view(), name='blog-home'),
