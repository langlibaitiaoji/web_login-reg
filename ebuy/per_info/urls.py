from django.urls import path, re_path
from . import views

app_name = 'per_info'
urlpatterns = [
    path('info_main/', views.info_main, name='info_main'),
    path('info_main/show_info', views.show_info, name='show_info'),
    path('info_main/modify_info', views.modify_info, name='modify_info'),
    path('info_main/modify_pwd', views.modify_pwd, name='modify_pwd'),
    path('info_main/handle_page_one', views.handle_page_one, name='handle_page_one'),
    re_path('info_main/handle_page_two/(?P<phone_number>[0-9]+)$', views.handle_page_two, name='handle_page_two'),
    re_path('info_main/handle_page_three/(?P<phone_number>[0-9]+)$', views.handle_page_three, name='handle_page_three'),
    path('index/', views.test)
]
