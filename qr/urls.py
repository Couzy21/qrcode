from django.urls import path
from .views import home, login_view, signup
app_name = 'qr'
urlpatterns = [
    path("home/", home, name="home"),
    path('login/', login_view, name="login"),
    path('signup/', signup, name="signup"),
]
