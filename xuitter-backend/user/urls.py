from django.urls import path, include
from user.views import ContactView, LoginView, LogoutView, SignupView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("<int:user_pk>/contacts", ContactView.as_view(), name="user-contacts"),
    path("post/", include("post.urls")),
]
