from django.urls import path, include
from user.views import LoginView, SignupView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('post/', include('post.urls'))
]