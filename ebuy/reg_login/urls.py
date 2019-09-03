from django.urls import path, re_path
from . import views

app_name = 'reg_login'
urlpatterns = [
    path('', views.dispatcher),
    path('index/', views.index, name='index'),
    path('reg_login/login', views.login, name='login'),
    path('reg_login/reg', views.reg, name='reg'),
    path('reg_login/handle_reg', views.handle_reg, name='handle_reg'),
    path('reg_login/handle_login', views.handle_login, name='handle_login'),
    path('reg_login/logout', views.logout, name='logout')
]
