from django.urls import path
from . import views

urlpatterns = [
    
    path('login/', views.login, name = "login"),
    path('register/', views.register, name = "register"),
    path('', views.home, name = "home"),
    path('logout', views.logout, name="logout"),
    path('profile/<str:pk>/', views.profile, name='profile'),
    path('follow', views.follow, name='follow'),
    path('like-post', views.like_post, name="like-post"),
    path('settings', views.settings, name="settings"),
    path('upload', views.upload, name="upload"),
    path('comment', views.comment, name="comment"),

]
