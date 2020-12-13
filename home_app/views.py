from django.shortcuts import render,redirect
from .forms import RegistrationForm
from Accounts.models import Account
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password,check_password

from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from Accounts.models import *
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth import logout
from profile_app.models import *

from django.views.decorators.csrf import csrf_exempt

import random


#from django.shortcuts import render_to_response
from django.template import RequestContext


'''def handler404(request, *args, **argv):
    response = render(request,'home_templates/404.html')
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request,'home_templates/500.html',)

    response.status_code = 500
    return response'''



@user_passes_test(lambda u: u.is_superuser)
def f_send(request,iid):
    obj         = Requested_Fund.objects.get(id=iid)
    account_obj = Account.objects.get(username = obj.user_name)

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
            return redirect('http://www.finderinternational.world/admin/profile_app/requested_fund/')
        else:
            return redirect('http://www.finderinternational.world/admin/profile_app/requested_fund/')


    else:
        pass
    return render(request,'home_templates/cancel.html')

@user_passes_test(lambda u: u.is_superuser)
def f_cancel(request,iid):
    obj         = Requested_Fund.objects.get(id=iid)
    account_obj = Account.objects.get(username = obj.user_name)

    if Fund.objects.filter(user = account_obj).exists():
        obj.status = 'Canceled'
        obj.save()
        return redirect('http://www.finderinternational.world/admin/profile_app/requested_fund/')

    else:
        pass

    return render(request,'home_templates/cancel.html')










@user_passes_test(lambda u: u.is_superuser)
def cancel_withrawal(request,iid):
    obj         = All_Withrawal_Request1.objects.get(id=iid)
    user        = Account.objects.get(username=obj.user.username)
    obj1        = All_Withrawal.objects.get(user = user , status='Pending')
    obj1.status = 'Canceled'
    user.refund += obj1.amount
    obj1.save()
    obj.delete()
    user.save()

    return redirect('http://www.finderinternational.world/admin/Accounts/all_withrawal_request1/')

    return render(request,'home_templates/cancel.html')

@user_passes_test(lambda u: u.is_superuser)
def accept_withrawal(request,iid):
    obj         = All_Withrawal_Request1.objects.get(id=iid)
    user        = Account.objects.get(username=obj.user.username)
    obj1        = All_Withrawal.objects.get(user = user , status='Pending')
    obj1.status = 'Approved'
    obj1.save()
    obj.delete()

    return redirect('http://www.finderinternational.world/admin/Accounts/all_withrawal_request1/')

    return render(request,'home_templates/cancel.html')







@login_required
def detail(request):
    username = request.session['user_name']
    sponser = request.session['spn']
    u_pass  = request.session['u_pass']
    txn_pass  = request.session['txn_pass']
    user_obj = Account.objects.get(username=username)
    spn_obj = Account.objects.get(username=sponser)


    d = {
        'username' : username,
        'sponser'  : sponser,
        'user_obj' : user_obj,
        'spn_obj' : spn_obj,
        'u_pass'   : u_pass,
        'txn_pass' : txn_pass,
        }
    return render(request, 'home_templates/detail.html',d)


def index(request):
    return render(request, 'home_templates/index.html')

def about(request):
    return render(request, 'home_templates/about.html')


def contact(request):
    return render(request, 'home_templates/contact.html')

@csrf_exempt
def login1(request):
    if request.method == 'POST':
        u_name = request.POST.get('user_name')
        pass1 = request.POST.get('pass_word')


        user = auth.authenticate(username=u_name,password=pass1)

        if user is not None:
            auth.login(request,user)
            return redirect('profile')
        else:
            messages.error(request,'Wrong username or password!!')
            return redirect('login')

    return render(request,'home_templates/login.html')

@csrf_exempt
def register(request):
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        sponser = request.POST.get('sponser')
        mobile_no = request.POST.get('mobile')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        print(pass1,pass2)

        pass12 = make_password(pass1)

        if pass1 != pass2:

            try:
                spn_obj = Account.objects.get(username=sponser)
                c = Account.objects.all().count()
                k = c + 2

                while True:
                    rand_num = random.randint(500000,599999)
                    u_name = 'FI' + str(rand_num)
                    if Account.objects.filter(username=u_name).exists():
                        pass
                    else:
                        break



                #u_name = 'FI9050' + str(k)



                '''obj = Account.objects.get(downline=None)
                upline_name = obj.username
                print(u_name)'''

                user = Account(username = u_name, sponser=sponser,password=pass12,email=email,txn_password=pass2,phon_no=mobile_no,rem_paas=pass1)
                #obj.downline = u_name

                user.save()
                
                request.session['user_name'] = u_name
                request.session['spn'] = sponser
                request.session['u_pass'] = pass1
                request.session['txn_pass'] = pass2

                user = auth.authenticate(username=u_name,password=pass1)
                if user is not None:
                    auth.login(request,user)


                messages.success(request,'Update Profile First!!')
                return redirect('detail')


            except Exception as e:
                print(e)
                messages.error(request,"Sponser Does Not Exist!!")
                return redirect('register')
        else:
            messages.error(request,'Password and transection password can not be same!!')
            return redirect('register')

    else:
        pass


    return render(request, 'home_templates/register.html')
