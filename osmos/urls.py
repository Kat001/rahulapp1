from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static
from home_app import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('detail/', views.detail,name='detail'),
    path('',include('home_app.urls')),
    path('admin1/',include('admin_panel.urls')),
    path('payment/',include('paymyment_gateway.urls')),



    path('profile/',include('profile_app.urls')),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='home_templates/password_reset.html'), name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='home_templates/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='home_templates/password_reset_confirm.html'), name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='home_templates/password_reset_complete.html'), name='password_reset_complete'),
]


'''handler404 = 'home_app.views.handler404'
handler500 = 'home_app.views.handler500'''

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
