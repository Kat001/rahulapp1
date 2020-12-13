import django_filters
from Accounts.models import  *
from profile_app.models import *



class Fund_requests_Filter1(django_filters.FilterSet):
    class Meta:
        model = Fund_History
        fields = ['user_name']

class All_Withrawal_requets_Filter1(django_filters.FilterSet):
    class Meta:
        model = All_Withrawal_Request1
        fields = ['user']

class All_Withrawal_Filter1(django_filters.FilterSet):
    class Meta:
        model = All_Withrawal
        fields = ['user']

    @property
    def username(self):
        return self.user.username
