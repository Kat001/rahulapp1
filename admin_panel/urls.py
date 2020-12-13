from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index, name='admin_index'),
    path('all_users',views.all_users, name='all_users'),

    path('edit/<int:iid>',views.edit,name='edit'),
    path('block/<int:iid>',views.block,name='block'),
    path('unblock/<int:iid>',views.unblock,name='unblock'),

    path('genrate_fund',views.genrate_fund,name='genrate_fund'),
    path('add_news',views.add_news,name='add_news'),


    path('withrawal_requests',views.withrawal_requests,name='withrawal_requests'),
    path('withrawal_requests_history',views.withrawal_requests_history,name='withrawal_requests_history'),

    path('aaccept_withrawal/<int:iid>',views.aaccept_withrawal,name='aaccept_withrawal'),
    path('acancel_withrawal/<int:iid>',views.acancel_withrawal,name='acancel_withrawal'),

    path('asend_fund/<int:iid>',views.asend_fund,name='asend_fund'),
    path('acancel_fund/<int:iid>',views.acancel_fund,name='acancel_fund'),

    path('fund_requests',views.fund_requests,name='fund_requests'),
    path('fund_requests_history',views.fund_requests_history,name='fund_requests_history'),

]
