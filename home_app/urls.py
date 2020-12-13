from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index, name='index'),
    path('super_user/<int:iid>', views.cancel_withrawal, ),
    path('super_user/accept/<int:iid>', views.accept_withrawal, ),

    path('super_user/f_cancel/<int:iid>', views.f_cancel, name='f_cancel' ),
    path('super_user/f_send/<int:iid>', views.f_send, name='f_send' ),


    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),


    path('register/',views.register, name='register'),
    path('login/',views.login1, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='home_templates/logout.html'),name='logout'),

]
