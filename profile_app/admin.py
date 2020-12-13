from django.contrib import admin
from .models import Fund,Requested_Fund
from Accounts.models import Account
from .models import *
from django.utils.html import format_html

# Register your models here.
class Fund_Admin(admin.ModelAdmin):
	list_display 		= ('username','available_fund')
	search_fields 		= ('username',)
	list_filter 		= ()
	fieldsets 			= ()

	'''def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False'''


class Fund_History_Admin(admin.ModelAdmin):
	list_display 		= ('user_name','activated_id','date','amount')
	search_fields 		= ('user_name',)
	list_filter 		= ()
	fieldsets 			= ()

	'''def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False'''


class RequestFund_Admin(admin.ModelAdmin):
	list_display = ('user_name','date','fund','transection_no','proof','status','cancel_fund','send_fund')
	search_fields = ('user_name',)
	#readonly_fields = ('user_name','date')
    #filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_funds','cancel_funds']

	def cancel_fund(self, obj):
		a = 'http://www.finderinternational.world/super_user/f_cancel/'+ str(obj.id)
		return format_html('<a href="{}" style="color:white;background-color:red">Cancel Fund</a>',a)

	def send_fund(self,obj):
		a = 'http://www.finderinternational.world/super_user/f_send/'+ str(obj.id)
		return format_html('<a href="{}" style="color:white;background-color:green;width:30px;height:20px;">Send Fund</a>',a)


	def send_funds(self, request, queryset):
		for obj in queryset:
			if obj.status=='Pending':
				name = obj.user_name
				r_fund = obj.fund
				user_obj = Account.objects.get(username=name)
				fund_obj = Fund.objects.get(user=user_obj)
				fund_obj.available_fund += r_fund
				obj.status = 'Approved'
				fund_obj.save()
				obj.save()

	def cancel_funds(self,request,queryset):
		queryset.update(status="Cancelled")

class Rank_1_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	#readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']



	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False
	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=0.50,rank=1)
				obj.day -= 1

				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 0.50
				user_obj.refund += 0.50

				user_obj.save()
				obj.save()
				income_obj.save()




class Rank_2_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	#readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False



	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=0.75,rank=2)
				#user.refund += 0.75
				obj.day -= 1

				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 0.75
				user_obj.refund += 0.75

				user_obj.save()
				obj.save()
				income_obj.save()


class Rank_3_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	#readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False


	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=1.25,rank=3)
				#user.refund += 1.25
				obj.day -= 1

				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 1.25
				user_obj.refund += 1.25
				obj.save()
				user_obj.save()
				income_obj.save()



class Rank_4_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	#readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False

	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
			    #user.refund += 2
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=2,rank=4)
				obj.day -= 1

				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 2
				user_obj.refund += 2

				user_obj.save()
				obj.save()
				income_obj.save()




class Rank_5_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	#readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False

	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
			    #user.refund += 5
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=5,rank=5)
				obj.day -= 1

				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 5
				user_obj.refund += 5

				user_obj.save()
				obj.save()
				income_obj.save()



class Rank_6_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	#readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False

	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
			    #user.refund += 8
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=8,rank=6)
				obj.day -= 1

				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 8
				user_obj.refund += 8

				user_obj.save()
				obj.save()
				income_obj.save()



class Rank_7_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	#readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False

	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
			    #user.refund += 15
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=15,rank=7)
				obj.day -= 1

				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 15
				user_obj.refund += 15

				user_obj.save()
				obj.save()
				income_obj.save()



class Rank_8_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	##readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False

	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
			    #user.refund += 40
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=40,rank=8)
				obj.day -= 1

				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 40
				user_obj.refund += 40

				user_obj.save()
				obj.save()
				income_obj.save()



class Rank_9_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	##readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False

	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
			    #user.refund += 70
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=70,rank=9)
				obj.day -= 1


				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 70
				user_obj.refund += 70

				user_obj.save()
				obj.save()
				income_obj.save()

class Rank_10_User_Admin(admin.ModelAdmin):
	list_display = ('username','achieve_date','day')
	search_fields = ('username',)
	##readonly_fields = ('username','date')
	#filter_horizontal = ()
	list_filter = ()
	fieldsets = ()
	actions = ['send_income']

	def has_delete_permission(self,request,obj=None):
		return False
	def has_add_permission(self,request,obj=None):
		return False


	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.day != 0:
			    #user = obj.user
			    #user.refund += 150
				income_obj = All_Rank_Income(user_name=obj.user.username,amount=150,rank=10)
				obj.day -= 1


				user_obj = Account.objects.get(username=obj.username)
				user_obj.total_rank_income += 150
				user_obj.refund += 150

				user_obj.save()
				obj.save()
				income_obj.save()




class All_Rank_Income_Admin(admin.ModelAdmin):
	list_display 		= ('user_name','date','amount',)
	search_fields 		= ('user_name',)
	list_filter 		= ()
	fieldsets 			= ()


class All_Level_Income_Admin(admin.ModelAdmin):
	list_display 		= ('user_name','activated_id','level','date','amount')
	search_fields 		= ('user_name',)
	list_filter 		= ()
	fieldsets 			= ()

class All_Direct_Income_Admin(admin.ModelAdmin):
	list_display 		= ('user_name','date','amount')
	search_fields 		= ('user_name',)
	list_filter 		= ()
	fieldsets 			= ()

class All_Roi_Income_Admin(admin.ModelAdmin):
	list_display 		= ('user_name','date','amount')
	search_fields 		= ('user_name',)
	list_filter 		= ()
	fieldsets 			= ()

class Bank_Info_Admin(admin.ModelAdmin):
	list_display 		= ('username','account_holder_name','account_number')
	search_fields 		= ('user_name',)
	list_filter 		= ()
	fieldsets 			= ()

	'''def has_delete_permission(self,request,obj=None):
		return False

	def has_add_permission(self,request,obj=None):
		return False'''

class Update_Roi_Income_Admin(admin.ModelAdmin):
	list_display 		= ('username','date','amount','days')
	search_fields 		= ('username',)
	list_filter 		= ()
	fieldsets 			= ()
	actions             = ['send_income']

	def send_income(self, request, queryset):
		for obj in queryset:
			if obj.days>0:
				obj.days -= 1

				d = 0
				if obj.amount == 1000:
					d = 20 #2%
				elif obj.amount == 5000:
					d = 100 #2%
				elif obj.amount == 10000:
					d = 250 #2.5%
				elif obj.amount == 25000:
					d = 750 #3%
				elif obj.amount == 50000:
					d = 2000 #4%
				elif obj.amount == 100000:
					d = 5000 #5%


				r_obj = All_Roi_Income(user_name=obj.username,amount=d)
				account_obj = Account.objects.get(username=obj.username)
				account_obj.refund += d
				account_obj.total_roi_income += d
				account_obj.save()
				r_obj.save()
				obj.save()


	'''def has_delete_permission(self,request,obj=None):
		return False

	def has_add_permission(self,request,obj=None):
		return False'''






admin.site.register(Fund,Fund_Admin)
admin.site.register(Update_Roi_Income,Update_Roi_Income_Admin)
#admin.site.register(All_Rank_Income,All_Rank_Income_Admin)
admin.site.register(Requested_Fund,RequestFund_Admin)

admin.site.register(Bank_Info,Bank_Info_Admin)

admin.site.register(All_Direct_Income,All_Direct_Income_Admin)
admin.site.register(All_Level_Income,All_Level_Income_Admin)
admin.site.register(All_Roi_Income,All_Roi_Income_Admin)

'''admin.site.register(Rank_1_User,Rank_1_User_Admin)
admin.site.register(Rank_2_User,Rank_2_User_Admin)
admin.site.register(Rank_3_User,Rank_3_User_Admin)
admin.site.register(Rank_4_User,Rank_4_User_Admin)
admin.site.register(Rank_5_User,Rank_5_User_Admin)
admin.site.register(Rank_6_User,Rank_6_User_Admin)
admin.site.register(Rank_7_User,Rank_7_User_Admin)
admin.site.register(Rank_9_User,Rank_9_User_Admin)
admin.site.register(Rank_8_User,Rank_8_User_Admin)
admin.site.register(Rank_10_User,Rank_10_User_Admin)'''
