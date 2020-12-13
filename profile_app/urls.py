from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.profile, name='profile'),
    path('user_profile/', views.user_profile, name = 'user_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),

    path('update_kyc/', views.update_kyc, name='update_kyc'),

    path('change_password/', views.change_password, name='change_password'),
    path('change_t_password/', views.change_t_password, name='change_t_password'),

    path('fund_request/', views.fund_request, name='fund_request'),
    path('fund_transfer/', views.fund_transfer, name='fund_transfer'),
    path('fund_transfer_history/', views.fund_transfer_history, name='fund_transfer_history'),

    path('direct_team/', views.direct_team, name='direct_team'),
    path('single_team/', views.single_team, name='single_team'),
    path('level_team/', views.level_team, name='level_team'),
    path('level_team2/', views.level_team2, name='level_team2'),
    path('level_team3/', views.level_team3, name='level_team3'),
    path('level_team4/', views.level_team4, name='level_team4'),
    path('level_team5/', views.level_team5, name='level_team5'),
    path('level_team6/', views.level_team6, name='level_team6'),
    path('level_team7/', views.level_team7, name='level_team7'),

    path('rank_income/', views.rank_income, name='rank_income'),
    path('direct_income/', views.direct_income, name='direct_income'),
    path('level_income/', views.level_income, name='level_income'),
    path('cti_income/', views.cti_income, name='cti_income'),

    path('withrawal_request/', views.withrawal_request, name='withrawal_request'),
    path('all_withrawal_request/', views.all_withrawal_request, name='all_withrawal_request'),



    path('activate_id/', views.activate_id, name='activate_id'),
    path('tet/', views.tet, name='tet'),

]
