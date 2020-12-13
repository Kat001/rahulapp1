from django.contrib import admin
from .models import Account
from .models import *
from django.contrib.auth.admin import UserAdmin
from profile_app.models import *

from django.utils.html import format_html
from django.urls import reverse
# from django.urls import url
from django.conf.urls import include, url
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse

from django.urls import reverse
from django.utils.http import urlencode

from django.contrib.auth.models import Group


# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('username', 'email', 'sponser', 'is_active1', 'date_active')
    search_fields = ('email', 'username',)
    readonly_fields = ('sponser','username','downline','upline')
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    actions = ['assign_ranks']

    '''def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False'''



    def assign_ranks(self, request, queryset):
        for obj in queryset:
            # First rank......
            user = Account.objects.get(username=obj.username)
            if Rank_1_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 125:
                    rank1 = Rank_1_User(user=user)
                    rank1.save()

            # Second Rank....
            if Rank_2_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 400:
                    rank1 = Rank_2_User(user=user)
                    rank1.save()

            # Third Rank...
            if Rank_3_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 950:
                    rank1 = Rank_3_User(user=user)
                    rank1.save()

            # Fourth Rank....
            if Rank_4_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 2050:
                    rank1 = Rank_4_User(user=user)
                    rank1.save()

            # Fifth Rank...
            if Rank_5_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 4850:
                    rank1 = Rank_5_User(user=user)
                    rank1.save()

            # Sixth Rank....
            if Rank_6_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 11950:
                    rank1 = Rank_6_User(user=user)
                    rank1.save()

            # Seventh Rank.....
            if Rank_7_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 23950:
                    rank1 = Rank_7_User(user=user)
                    rank1.save()

            # Eighth Rank...
            if Rank_8_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 50950:
                    rank1 = Rank_8_User(user=user)
                    rank1.save()

            # 9th rank...
            if Rank_9_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 105950:
                    rank1 = Rank_9_User(user=user)
                    rank1.save()

            # 10th Rank.....
            if Rank_10_User.objects.filter(user=user).exists():
                pass
            else:
                if obj.down_team >= 226950:
                    rank1 = Rank_10_User(user=user)
                    rank1.save()



class All_Withrawal_Request1_Admin(admin.ModelAdmin):
    list_display = ('username', 'date', 'account_holder_name', 'account_number', 'ifsc_code', 'branch_name', 'amount','Rupya',
                    'accept_withrawal', 'cancel_withrawal',)
    search_fields = ('username',)
    list_filter = ()
    fieldsets = ()

    def Rupya(self,obj):
        return obj.w_amount*75


    def has_delete_permission(self,request,obj=None):
        return False

    def has_add_permission(self,request,obj=None):
            return False




    def cancel_withrawal(self, obj):
        a = 'http://www.finderinternational.world/super_user/'+ str(obj.id)

        return format_html('<a href="{}" style="color:white;background-color:red">Cancel</a>',a)

    def accept_withrawal(self,obj):
        a = 'http://www.finderinternational.world/super_user/accept/'+ str(obj.id)

        return format_html('<a href="{}" style="color:white;background-color:green;width:30px;height:20px;">Accept</a>',a)


class All_Withrawal_Admin(admin.ModelAdmin):
    list_display = ('username', 'date', 'account_holder_name', 'account_number', 'ifsc_code', 'branch_name', 'amount','status',)
    search_fields = ('username',)
    list_filter = ()
    fieldsets = ()

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.unregister(Group)
admin.site.register(Account, AccountAdmin)
admin.site.register(All_Withrawal_Request1, All_Withrawal_Request1_Admin)
admin.site.register(All_Withrawal, All_Withrawal_Admin)

'''
<div class="col-lg-6 mb-4">
<div class="card bg-warning text-white shadow">
<div class="card-body">
Warning
<div class="text-white-50 small">#f6c23e</div>
</div>
</div>
</div>
<div class="col-lg-6 mb-4">
<div class="card bg-danger text-white shadow">
<div class="card-body">
Danger
<div class="text-white-50 small">#e74a3b</div>
</div>
</div>
</div>
<div class="col-lg-6 mb-4">
<div class="card bg-secondary text-white shadow">
<div class="card-body">
Secondary
<div class="text-white-50 small">#858796</div>
</div>
</div>
</div>
<div class="col-lg-6 mb-4">
<div class="card bg-light text-black shadow">
<div class="card-body">
Light
<div class="text-black-50 small">#f8f9fc</div>
</div>
</div>
</div>

</div>
</div>



'''
