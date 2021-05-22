from django.contrib import admin
from django.urls import path
from . import views
from .views import AllPostListView, PostDetailView, CreateNewPost, PostUpdateView, PostDeleteView, UserAllPostListView, CommentsView, CommentDetailView, CommentUpdateView,CommentDeleteView,PostRestApi

urlpatterns = [
    path('',AllPostListView.as_view(), name='Home'),
    path('post/<int:pk>/',PostDetailView.as_view(), name='post-detail'),
    path('new/',CreateNewPost.as_view(), name='new-post'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>/post/', UserAllPostListView.as_view(), name='user-post'),
    path('post/<int:pk>/comments/',CommentsView.as_view(),name='add-comment'),
    path('post/<int:pk>/responses/', CommentDetailView.as_view(), name='responses'),
    path('response/<int:pk>/update_Comment/', CommentUpdateView.as_view(), name='comment-update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    path('about/',views.about_view, name='About'),
    path('api/<str:help_type>/', PostRestApi.as_view(), name='post-api')
]
