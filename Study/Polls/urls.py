from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.main, name="main"),
    path('login/', views.auth, name="login"),
    path('register/', views.register_view, name="register"),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
]