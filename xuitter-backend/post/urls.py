from django.urls import path
from post.views import PostView, PostActionView

urlpatterns = [
    path('', PostView.as_view(), name='post'),
    path('<int:pk>/', PostView.as_view(), name='post-detail'),
    path('<int:pk>/action/', PostActionView.as_view(), name='post-action')
]