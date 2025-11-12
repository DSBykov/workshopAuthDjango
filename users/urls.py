from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login', views.login_view, name='login'),
    path('signin', views.signin_view, name='signin'),
    path('logout-confirm', views.logout_confirm, name='logout-confirm'),
    path('logout', LogoutView.as_view(), name='logout'),
]