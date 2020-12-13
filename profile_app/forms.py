from django import forms
from .models import Requested_Fund,Bank_Info
from admin_panel.models import News

class News_Form(forms.ModelForm):
	class Meta:
		model = News
		fields = '__all__'

class Requested_Fund_Form(forms.ModelForm):
	#user_name = forms.CharField(disabled=True)

	class Meta:
		model = Requested_Fund
		fields = ['user_name','date','fund','transection_no','proof']

class Bank_Form(forms.ModelForm):
	class Meta:
		model = Bank_Info
		fields =['account_holder_name','account_number','ifsc_code','bank_name','branch_name','nominee_name','aadhar_number','pan_number','aadhar_image','pan_image']
