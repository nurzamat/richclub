from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('', views.index, name='index'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('signup', views.signup, name='signup'),
    path('home', views.home, name='home'),
    path('structure', views.structure, name='structure'),
    path('invited', views.invited, name='invited'),
    path('invited_ajax', views.invited_ajax, name='invited_ajax'),
    path('bonus_history', views.bonus_history, name='bonus_history'),
    path('validate_username_ajax', views.validate_username_ajax, name='validate_username_ajax'),
    path('documentation', views.documentation, name='documentation'),
    path('notifications', views.notifications, name='notifications'),
]

