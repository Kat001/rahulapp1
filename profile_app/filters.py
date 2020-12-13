import django_filters
from Accounts.models import  *
from .models import *

class Account_Filter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = ['username']

class Direct_Income_Filter(django_filters.FilterSet):
    class Meta:
        model = All_Direct_Income
        fields = ['activated_id']

class Rank_Income_Filter(django_filters.FilterSet):
    class Meta:
        model = All_Rank_Income
        fields = ['rank']

class Level_Income_Filter(django_filters.FilterSet):
    class Meta:
        model = All_Level_Income
        fields = ['activated_id']

class Fund_History_Filter(django_filters.FilterSet):
    class Meta:
        model = Fund_History
        fields = ['activated_id']

class All_Withrawal_Filter(django_filters.FilterSet):
    class Meta:
        model = All_Withrawal
        fields = ['status']
