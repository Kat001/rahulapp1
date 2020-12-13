from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test
from Accounts.models import *
from profile_app.filters import *
from admin_panel.filters import *
from django.contrib import messages

from profile_app.forms import News_Form
from .models import *

# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
def add_news(request):
    form = News_Form()
    if request.method=='POST':
        form = News_Form(request.POST)
        if form.is_valid():
            obj = News.objects.all().delete()
            form.save()

    d = {
        'form':form,
    }
    return render(request,'admin_templates/add_news.html',d)

@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request,'admin_templates/index.html')

@user_passes_test(lambda u: u.is_superuser)
def all_users(request):
    user = request.user
    objs = Account.objects.all().exclude(username='admin')
    banks = Bank_Info.objects.all().exclude(user=user)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'banks':banks,
        'myfilter':myfilter,
    }

    return render(request,'admin_templates/all_users.html',d)

def edit(request,iid):
    link = '/admin/Accounts/account/' + str(iid) + '/change/'
    return redirect(link)
    return render(request,'admin_templates/all_users.html')

def block(request,iid):
    obj = Account.objects.get(id = iid)
    obj.is_active = False
    obj.save()
    messages.success(request,'Deactivated successfully!!')
    return redirect('all_users')
    return render(request,'admin_templates/all_users.html')

def unblock(request,iid):
    obj = Account.objects.get(id = iid)
    obj.is_active = True
    obj.save()
    messages.success(request,'Activated successfully!!')
    return redirect('all_users')
    return render(request,'admin_templates/all_users.html')

def genrate_fund(request):
    user = request.user
    fund_obj = Fund.objects.get(user=user)
    if request.method=='POST':
        f = request.POST.get('avail_fund')
        fund_obj.available_fund += float(f)
        fund_obj.save()
        messages.success(request,'Fund Added successfully!!')
        return redirect('genrate_fund')

    d = {
        'fund_obj' : fund_obj
    }
    return render(request,'admin_templates/genrate_fund.html',d)


@user_passes_test(lambda u: u.is_superuser)
def withrawal_requests(request):
    objs = All_Withrawal_Request1.objects.all()

    myfilter = All_Withrawal_requets_Filter1(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter,
    }
    return render(request,'admin_templates/withrawal_requests.html',d)

@user_passes_test(lambda u: u.is_superuser)
def aaccept_withrawal(request,iid):
    obj         = All_Withrawal_Request1.objects.get(id=iid)
    user        = Account.objects.get(username=obj.user.username)
    obj1        = All_Withrawal.objects.get(user = user , status='Pending')
    obj1.status = 'Approved'
    obj1.save()
    obj.delete()
    messages.success(request,'successfull!!')
    return redirect('withrawal_requests')
    return render(request,'admin_templates/index.html')


@user_passes_test(lambda u: u.is_superuser)
def acancel_withrawal(request,iid):
    obj         = All_Withrawal_Request1.objects.get(id=iid)
    user        = Account.objects.get(username=obj.user.username)
    obj1        = All_Withrawal.objects.get(user = user , status='Pending')
    obj1.status = 'Canceled'
    user.refund += obj1.amount
    obj1.save()
    obj.delete()
    user.save()
    return redirect('withrawal_requests')

    return render(request,'admin_templates/index.html')

def withrawal_requests_history(request):
    objs = All_Withrawal.objects.all()

    myfilter = All_Withrawal_Filter1(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter,
    }
    return render(request,'admin_templates/withrawal_requests_history.html',d)

@user_passes_test(lambda u: u.is_superuser)
def fund_requests(request):
    objs = Requested_Fund.objects.filter(status='Pending')

    myfilter = Fund_requests_Filter1(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter
    }
    return render(request,'admin_templates/fund_requests.html',d)

@user_passes_test(lambda u: u.is_superuser)
def asend_fund(request,iid):
    obj         = Requested_Fund.objects.get(id=iid)

    try:
        account_obj = Account.objects.get(username = obj.user_name)
    except Exception as e:
        obj.delete()

        messages.error(request,'User does not Exists(Cancel)!!')
        return redirect('fund_requests')

    if Fund.objects.filter(user = account_obj).exists():
        if obj.status=='Pending':
            name = obj.user_name
            r_fund = obj.fund
            user_obj = Account.objects.get(username=name)
            fund_obj = Fund.objects.get(user=user_obj)
            fund_obj.available_fund += r_fund
            obj.status = 'Approved'
            fund_obj.save()
            obj.save()
            messages.success(request,'Fund Sended Successfully!!')
            return redirect('fund_requests')


    else:
        obj.delete()
        messages.error(request,'User does not exists(Canceled)!!')
    d = {

    }
    return render(request,'admin_templates/fund_requests.html',d)

@user_passes_test(lambda u: u.is_superuser)
def acancel_fund(request,iid):
    obj         = Requested_Fund.objects.get(id=iid)

    try:
        account_obj = Account.objects.get(username = obj.user_name)
    except Exception as e:
        obj.delete()

        messages.error(request,'User does not Exists(Cancel)!!')
        return redirect('fund_requests')

    obj.status = 'Canceled'
    obj.save()
    messages.error(request,'canceled Successfully!!')

    d = {

    }
    return render(request,'admin_templates/fund_requests.html',d)

@user_passes_test(lambda u: u.is_superuser)
def fund_requests_history(request):
    objs = Requested_Fund.objects.all()


    myfilter = Fund_requests_Filter1(request.GET,queryset=objs)
    objs  = myfilter.qs


    d = {
        'objs' : objs,
        'myfilter':myfilter
    }
    return render(request,'admin_templates/fund_requests_history.html',d)
