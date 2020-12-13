from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from .models import Requested_Fund,Fund,All_Rank_Income
from .forms import Requested_Fund_Form,Bank_Form
from Accounts.models import *
from .models import *

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import update_session_auth_hash
from django.core.files.storage import FileSystemStorage

from .filters import *

import datetime
from datetime import date

from django.db.models import Sum

from admin_panel.models import News





# Create your views here.

@login_required
def profile(request):
    user = request.user
    team = user.down_team
    fund = Fund.objects.get(user=user)

    '''a = Account.objects.get(username='dev')
    a.sponser=''
    a.save()'''

    direct = Account.objects.filter(sponser=user.username,is_active1=True).count()
    w_obj = list(All_Withrawal.objects.filter(user=user,status='Approved').aggregate(Sum('amount')).values())[0]
    print(w_obj)
    news_obj = News.objects.all()


    d = {
        'user' : user,
        'team' : team,
        'direct':direct,
        'fund' : fund,
        'w_obj' : w_obj,
        'news_obj':news_obj,
        }
    return render(request, 'profile_templates/index.html',d)

def tet(request):
    ##Account.objects.get(username='dev').delete()


    return render(request,'profile_templates/index.html')



@login_required
def fund_request(request):
    user = request.user
    name1 = user.username
    today = date.today()

    try:
        form = Requested_Fund_Form(initial={'user_name': user.username,'date':today.strftime("%Y-%m-%d")})
        rqs =  Requested_Fund.objects.filter(user_name=name1)
        if request.method=='POST' or request.method is None:
            form = Requested_Fund_Form(request.POST,request.FILES)
            p = request.POST.get('txn_pass')
            u_txn = user.txn_password
            if form.is_valid:
                if p == u_txn:
                    form.save()
                    messages.success(request,'Request submitted successfully!!')
                    return redirect('fund_request')
                else:
                    messages.error(request,'Wrong Transection password')
                    return redirect('fund_request')

            else:
                messages.error(request,'Fill correct data!!')
                form = Requested_Fund_Form()
    except Exception as e:
        return redirect('fund_request')
    d = {
        'form' : form,
        'rqs' : rqs,
        'c' : 1,
        'user' : user
        }
    return render(request,'profile_templates/request_fund.html',d)


@login_required
def fund_transfer(request):
    user = request.user
    obj = Fund.objects.get(user=user)

    if request.method == 'POST':
        user_name       = request.POST.get('user_name')
        amount          = request.POST.get('amount')
        txn_pass        = request.POST.get('txn_pass')

        try:
            if user.txn_password == txn_pass:
                if user_name != user.username:
                    user1 = Account.objects.get(username=user_name)
                    u_id_obj = Fund.objects.get(user=user1)

                    if obj.available_fund >= int(amount):
                        u_id_obj.available_fund += int(amount)
                        obj.available_fund -= int(amount)
                        u_id_obj.save()
                        obj.save()

                        obj_hist = Fund_History(user_name=user.username,activated_id=user_name,amount=amount)
                        obj_hist.save()

                        messages.success(request,'Fund Transfered successfully!!')
                        return redirect('fund_transfer')

                    else:
                        messages.error(request,'Not Enough Amount!!')
                        return redirect('fund_transfer')
                else:
                    messages.error(request,'U entered your own id!!')
                    return render('fund_transfer')
            else:
                messages.error(request,'Wrong Txn Password!!')
        except Exception as e:
            print(e)
            messages.error(request,'User id does not exist!!')
            return redirect('fund_transfer')

    d = {
        'obj' : obj,
    }
    return render(request,'profile_templates/fund_transfer.html',d)

def fund_transfer_history(request):
    user = request.user
    objs = Fund_History.objects.filter(user_name=user.username)

    myfilter = Fund_History_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter': myfilter,
    }

    return render(request,'profile_templates/fund_transfer_history.html',d)

@login_required
def activate_id(request):
    user_obj = request.user
    fund_obj = Fund.objects.get(user = user_obj)
    avail_fund = fund_obj.available_fund

    try:
        if request.method == 'POST':
            price = request.POST.get('pack')
            user_name = request.POST.get('u_name')
            obj = Account.objects.get(username=user_name)

            p = request.POST.get('txn_pass')
            u_txn = user_obj.txn_password

            if p == u_txn:
                if obj.is_active1 == False:
                    if avail_fund >= float(price):
                        fund_obj.available_fund -= float(price)
                        obj.is_active1 = True
                        #print("worked")
                        obj.activation_amount += float(price)
                        obj.date_active = datetime.datetime.now()
                        obj.save()
                        fund_obj.save()

                        spnn_obj = Account.objects.get(username = obj.sponser)
                        spnn_obj.total_direct_income += (float(price)*10/100)
                        spnn_obj.save()
                        new_obj = All_Direct_Income(user_name=spnn_obj.username,activated_id=obj.username,amount=(float(price)*10/100))
                        new_obj.save()

                        d = 0
                        if int(price) == 1000:
                            d = 100 #2%
                        elif int(price) == 5000:
                            d = 100 #2%
                        elif int(price) == 10000:
                            d = 100 #2.5%
                        elif int(price) == 25000:
                            d = 90 #3%
                        elif int(price) == 50000:
                            d = 70 #4%
                        elif int(price) == 100000:
                            d = 60 #5%

                        roi_obj = Update_Roi_Income(user = obj,days=d,amount=float(price))
                        roi_obj.save()

                        i = 7
                        while obj.sponser != None and i!=0:
                            obj = Account.objects.get(username=obj.sponser)

                            if obj.is_active1:
                                if i==7:
                                    income = (float(price)*10/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='1',amount=income,activated_id=user_name)
                                    all_level_obj.save()
                                if i==6:
                                    income = (int(price)*5/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='2',amount=income,activated_id=user_name)
                                    all_level_obj.save()

                                if i==5:
                                    income = (int(price)*4/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='3',amount=income,activated_id=user_name)
                                    all_level_obj.save()
                                if i==4:
                                    income = (int(price)*3/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='4',amount=income,activated_id=user_name)
                                    all_level_obj.save()
                                if i==3:
                                    income = (int(price)*2/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='5',amount=income,activated_id=user_name)
                                    all_level_obj.save()
                                if i==2:
                                    income = (int(price)*1/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='6',amount=income,activated_id=user_name)
                                    all_level_obj.save()

                                if i==1:
                                    income = (int(price)*0.5/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='7',amount=income,activated_id=user_name)
                                    all_level_obj.save()

                                i = i - 1
                                obj.save()
                            else:
                                i = i-1
                        messages.success(request,'Activated successfully!!')
                        return redirect('activate_id')

                    else:
                        messages.error(request,'Not Enough balance!!')
                        return redirect('activate_id')
                else:
                    if avail_fund >= float(price):
                        fund_obj.available_fund -= float(price)
                        obj.activation_amount += float(price)
                        obj.save()
                        fund_obj.save()

                        spnn_obj = Account.objects.get(username = obj.sponser)
                        spnn_obj.total_direct_income += (float(price)*10/100)
                        spnn_obj.save()
                        new_obj = All_Direct_Income(user_name=spnn_obj.username,activated_id=obj.username,amount=(float(price)*10/100))
                        new_obj.save()


                        d = 0
                        if int(price) == 1000:
                            d = 100 #2%
                        elif int(price) == 5000:
                            d = 100 #2%
                        elif int(price) == 10000:
                            d = 100 #2.5%
                        elif int(price) == 25000:
                            d = 90 #3%
                        elif int(price) == 50000:
                            d = 70 #4%
                        elif int(price) == 100000:
                            d = 60 #5%

                        roi_obj = Update_Roi_Income(user = obj,days=d,amount=float(price))
                        roi_obj.save()


                        i = 7
                        while obj.sponser != None and i!=0:
                            obj = Account.objects.get(username=obj.sponser)

                            if obj.is_active1:
                                if i==7:
                                    income = (float(price)*10/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='1',amount=income,activated_id=user_name)
                                    all_level_obj.save()
                                if i==6:
                                    income = (float(price)*5/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='2',amount=income,activated_id=user_name)
                                    all_level_obj.save()

                                if i==5:
                                    income = (float(price)*4/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='3',amount=income,activated_id=user_name)
                                    all_level_obj.save()
                                if i==4:
                                    income = (float(price)*3/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='4',amount=income,activated_id=user_name)
                                    all_level_obj.save()
                                if i==3:
                                    income = (float(price)*2/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='5',amount=income,activated_id=user_name)
                                    all_level_obj.save()
                                if i==2:
                                    income = (float(price)*1/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='6',amount=income,activated_id=user_name)
                                    all_level_obj.save()

                                if i==1:
                                    income = (float(price)*0.5/100)
                                    obj.total_level_income += income
                                    obj.refund += income
                                    all_level_obj = All_Level_Income(user_name=obj.username,level='7',amount=0.25,activated_id=user_name)
                                    all_level_obj.save()

                                i = i - 1
                                obj.save()
                            else:
                                i = i-1
                        messages.success(request,'Activated successfully!!')
                        return redirect('activate_id')
                    else:
                        messages.error(request,'Not Enough balance!!')
                        return redirect('activate_id')


            else:
                messages.error(request,'Wrong transection password!!')
                return redirect('activate_id')

    except Exception as e:
        print(e)
        messages.error(request,'Id does not exist!!')
        return redirect('activate_id')

    d = {
        'fund' : avail_fund,
        }

    return render(request,'profile_templates/activate_id.html',d)

def user_profile(request):
	user = request.user
	d = {
		'user' : user,
	}
	return render(request,'profile_templates/user_profile.html',d)


def update_profile(request):
    user = request.user
    name = user.username
    if request.method == 'POST':
        f_name = request.POST.get('f_name')
        l_name = request.POST.get('l_name')
        mobile_no = request.POST.get('mobile')
        address = request.POST.get('address')
        state = request.POST.get('state')
        city = request.POST.get('city')
        zip = request.POST.get('zip')
        myfile = request.FILES['myfile']
        p = request.POST.get('txn_pass')

        user_obj = Account.objects.get(username=name)
        if p == user_obj.txn_password:
            user_obj.first_name = f_name
            user_obj.last_name = l_name
            user_obj.phon_no = mobile_no
            user_obj.address = address
            user_obj.state = state
            user_obj.city = city
            user_obj.zip = zip
            user_obj.image = myfile


            user_obj.save()


            messages.success(request,'Profile Updated successfully!!')
            return redirect('update_profile')
        else:
            messages.error(request,'Wrong Transection password!!')
            return redirect('update_profile')
    else:
        pass
    return render(request,'profile_templates/update_profile.html')

def change_password(request):
    user = request.user
    user_pass = user.password

    if request.method == 'POST':
        o_pass = request.POST.get('o_pass')
        n_pass = request.POST.get('n_pass')
        c_pass = request.POST.get('c_pass')

        cheak = user.check_password(o_pass)

        if cheak:
            if n_pass == c_pass:
                p = make_password(n_pass)
                obj = Account.objects.get(username=user.username)
                user.set_password(n_pass)
                user.save()
                update_session_auth_hash(request,user)
                messages.success(request,"Password Changed successfully!!")
                return redirect('change_password')
            else:
                messages.error(request,'New password and confirm password should be same!!')
                return redirect('change_password')
        else:
            messages.error(request,"Old Password is Wrong!!")
            return redirect('change_password')





    return render(request,'profile_templates/change_password.html')

def change_t_password(request):
    user = request.user
    user_t_pass = user.txn_password

    if request.method == 'POST':
        o_pass = request.POST.get('o_pass')
        n_pass = request.POST.get('n_pass')
        c_pass = request.POST.get('c_pass')

        if user_t_pass == o_pass:
            if n_pass == c_pass:
                user.txn_password = n_pass
                user.save()
                messages.success(request,'Txn password changed successfully!!')
            else:
                messages.error(request,'New password and confirm password should be same!!')
                return redirect('change_t_password')
        else:
            messages.error(request,'Old Txn Password is Wrong!!')
            return redirect('change_t_password')

    return render(request,'profile_templates/change_t_password.html')

def direct_team(request):
    user = request.user
    objs = Account.objects.filter(sponser=user.username)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'T' : True,
        'myfilter':myfilter
    }
    return render(request,'profile_templates/direct_team.html',d)

def single_team(request):
    user = request.user
    a = user.total_team
    a = a.split(',')

    l = []
    for i in a:
        try:
            i = int(i)
            #o = Account.objects.get(id=i)
            l.append(i)
        except Exception as e:
            pass

    objs = Account.objects.filter(id__in=l)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {


        'objs' : objs,
        'T' : True,
        'myfilter':myfilter
    }
    return render(request,'profile_templates/single_team.html',d)

def level_team(request):
    user = request.user

    objs = Account.objects.filter(sponser=user.username)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter

    }

    return render(request,'profile_templates/level_team.html',d)

def level_team2(request):
    user = request.user
    l = []

    objs1 = Account.objects.filter(sponser=user.username)

    for o in objs1:
        obj2 = Account.objects.filter(sponser=o.username)
        for i in obj2:
            l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter

    }
    return render(request,'profile_templates/level2.html',d)

def level_team3(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponser=user.username)

    for o in objs1:
        obj2 = Account.objects.filter(sponser=o.username)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponser=o2.username)
            for i in obj3:
                l.append(i.id)
    objs = Account.objects.filter(id__in=l)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter

    }
    return render(request,'profile_templates/level3.html',d)

def level_team4(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponser=user.username)

    for o in objs1:
        obj2 = Account.objects.filter(sponser=o.username)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponser=o2.username)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponser=o3.username)
                for i in obj4:
                    l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter

    }
    return render(request,'profile_templates/level4.html',d)

def level_team5(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponser=user.username)

    for o in objs1:
        obj2 = Account.objects.filter(sponser=o.username)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponser=o2.username)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponser=o3.username)
                for o4 in obj4:
                    obj5 = Account.objects.filter(sponser=o4.username)
                    for i in obj5:
                        l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter

    }
    return render(request,'profile_templates/level5.html',d)

def level_team6(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponser=user.username)

    for o in objs1:
        obj2 = Account.objects.filter(sponser=o.username)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponser=o2.username)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponser=o3.username)
                for o4 in obj4:
                    obj5 = Account.objects.filter(sponser=o4.username)
                    for o5 in obj5:
                        obj6 = Account.objects.filter(sponser=o5.username)
                        for i in obj6:
                            l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter

    }
    return render(request,'profile_templates/level6.html',d)

def level_team7(request):
    user = request.user
    l =[]


    objs1 = Account.objects.filter(sponser=user.username)

    for o in objs1:
        obj2 = Account.objects.filter(sponser=o.username)
        for o2 in obj2:
            obj3 = Account.objects.filter(sponser=o2.username)
            for o3 in obj3:
                obj4 = Account.objects.filter(sponser=o3.username)
                for o4 in obj4:
                    obj5 = Account.objects.filter(sponser=o4.username)
                    for o5 in obj5:
                        obj6 = Account.objects.filter(sponser=o5.username)
                        for o6 in obj6:
                            obj7 = Account.objects.filter(sponser=o6.username)
                            for i in obj7:
                                l.append(i.id)

    objs = Account.objects.filter(id__in=l)

    myfilter = Account_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter

    }
    return render(request,'profile_templates/level7.html',d)

def rank_income(request):
    user = request.user

    objs = All_Roi_Income.objects.filter(user_name=user.username)

    myfilter = Rank_Income_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs


    d = {
        'objs' : objs,
        'T' : True,
        'myfilter':myfilter,
    }
    return render(request,'profile_templates/rank_income.html',d)

def direct_income(request):
    user = request.user

    objs = All_Direct_Income.objects.filter(user_name=user.username)

    myfilter = Direct_Income_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'T' : True,
        'myfilter':myfilter
    }
    return render(request,'profile_templates/direct_income.html',d)

def level_income(request):
    user = request.user

    objs = All_Level_Income.objects.filter(user_name=user.username)
    myfilter = Direct_Income_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'T' : True,
        'myfilter':myfilter,
    }
    return render(request,'profile_templates/level_income.html',d)

def cti_income(request):
    return render(request,'profile_templates/cti_income.html')

def update_kyc(request):
    user_obj = request.user
    obj = Bank_Info.objects.get(user = user_obj)

    if request.method == 'POST':
        a_holdername = request.POST.get('name')
        a_number     = request.POST.get('number')
        ifsc     = request.POST.get('ifsc')
        branch     = request.POST.get('branch')
        b_name     = request.POST.get('bank')
        n_name     = request.POST.get('nominee')
        #a_no     = request.POST.get('aadhar')
        p_no     = request.POST.get('pan')
        #a_image     = request.FILES['myfile1']
        #p_image     = request.FILES['myfile2']
        p = request.POST.get('txn_pass')

        if p == user_obj.txn_password:
            if obj.cheak == False:
                obj.account_holder_name = a_holdername
                obj.account_number = a_number
                obj.ifsc_code = ifsc
                obj.branch_name = branch
                obj.bank_name = b_name
                obj.nominee_name = n_name
                obj.pan_number = p_no
                #obj.aadhar_number = a_no
                #obj.aadhar_image = a_image
                #obj.pan_image = p_image
                obj.cheak = True
                obj.save()
                messages.success(request,'Updated successfully!!')
                return redirect('update_kyc')
            else:
                messages.error(request,'Contact to admin!!')
                return redirect('update_kyc')
        else:
            messages.error(request,'Wrong Txn Password!!')
            return redirect('update_kyc')







    d = {

        'bank_obj':obj
        }
    return render(request,'profile_templates/update_kyc.html',d)


@login_required
def withrawal_request(request):
    user = request.user
    #total_amount = user.total_level_income + user.total_direct_income + user.total_rank_income + user.refund
    bank_obj = Bank_Info.objects.get(user=user)


    if request.method == 'POST':
        amount = request.POST.get('amount')
        txn_pass = request.POST.get('txn_pass')
        amount = int(amount)



        if txn_pass == user.txn_password:
            if bank_obj.cheak == True:
                cheak = All_Withrawal.objects.filter(user=user,status='Pending').count()
                if cheak == 0:
                    if amount>=300 and amount<=user.refund:
                        charge   = (amount * 10)/100
                        w_amount = amount-charge
                        obj11 = All_Withrawal_Request1(user=user,amount=amount,status='Pending',
                                                       account_number=bank_obj.account_number,
                                                       account_holder_name=bank_obj.account_holder_name,
                                                       ifsc_code = bank_obj.ifsc_code,
                                                       bank_name = bank_obj.bank_name,
                                                       charge=charge,w_amount=w_amount)

                        obj12 = All_Withrawal(user=user,amount=amount,status='Pending',
                                                       account_number=bank_obj.account_number,
                                                       account_holder_name=bank_obj.account_holder_name,
                                                       ifsc_code = bank_obj.ifsc_code,
                                                       bank_name = bank_obj.bank_name,
                                                       branch_name = bank_obj.branch_name,
                                                       charge=charge,w_amount=w_amount)
                        obj11.save()
                        obj12.save()

                        user.refund = user.refund-amount
                        user.save()
                        messages.success(request,'Request submitted successfully!!!')
                        return redirect('withrawal_request')

                    else:
                        messages.error(request,'Not Enough Balance!!')
                        return redirect('withrawal_request')
                else:
                    messages.error(request,'your  First request is in Pending!!')
                    return redirect('withrawal_request')
            else:
                messages.error(request,'Update KYC !!')
                return redirect('withrawal_request')
        else:
            messages.error(request,'Wrong Txn Password!!')
            return redirect('withrawal_request')

    d = {
        'refund'    : user.refund,
        'account_no': bank_obj.account_number,
    }
    return render(request,'profile_templates/withrawal_request.html',d)

def all_withrawal_request(request):
    user =request.user
    objs = All_Withrawal.objects.filter(user=user)

    myfilter = All_Withrawal_Filter(request.GET,queryset=objs)
    objs  = myfilter.qs

    d = {
        'objs' : objs,
        'myfilter':myfilter,
    }
    return render(request,'profile_templates/all_withrawal_request.html',d)

'''
if user.is_active1:
    direct = Account.objects.filter(sponser=user.username).count()
    d = Account.objects.filter(sponser=user.username).order_by('date_active')
    print(d)

    if direct >= 1:
        objs = Account.objects.filter(date_active__gt=d[0].date_active).count()
        if objs <= 150:
            team = objs
            try:
                d1 = d[1].date_active
            except Exception as e:
                pass


        else:
            team = 150
            obj1  = obj.objects.filter(date_active__gt=d[0].date_active).order_by('date_active')
            d1 = obj1[149].date_active

    if direct >= 2:
        if d[1].date_active <= d1:
            objs = Account.objects.filter(date_active__gt=d1).count()
            if objs <= 350:
                team += objs
                try:
                    d1 = d[2].date_active
                except Exception as e:
                    pass
            else:
                team += 350
                obj1  = obj.objects.filter(date_active__gt=d1).order_by('date_active')
                d1 = obj1[299].date_active


        else:
            objs = Account.objects.filter(date_active__gt=d[1].date_active).count()
            if objs <= 350:
                team += objs
                try:
                    d1 = d[2].date_active
                except Exception as e:
                    pass
            else:
                team += 350
                obj1  = obj.objects.filter(date_active__gt=d[1].date_active).order_by('date_active')
                d1 = obj1[299].date_active




    if direct >= 3:
        if d[2].date_active <= d1:
            objs = Account.objects.filter(date_active__gt=d1).count()
            if objs <= 800:
                team += objs
                try:
                    d1 = d[3].date_active
                except Exception as e:
                    pass
            else:
                team += 800
                obj1  = obj.objects.filter(date_active__gt=d1).order_by('date_active')
                d1 = obj1[299].date_active


        else:
            objs = Account.objects.filter(date_active__gt=d[2].date_active).count()
            if objs <= 800:
                team += objs
                try:
                    d1 = d[3].date_active
                except Exception as e:
                    pass
            else:
                team += 800
                obj1  = obj.objects.filter(date_active__gt=d[2].date_active).order_by('date_active')
                d1 = obj1[799].date_active


    if direct >= 4:
        if d[3].date_active <= d1:
            objs = Account.objects.filter(date_active__gt=d1).count()
            if objs <= 1500:
                team += objs
                try:
                    d1 = d[4].date_active
                except Exception as e:
                    pass
            else:
                team += 1500
                obj1  = obj.objects.filter(date_active__gt=d1).order_by('date_active')
                d1 = obj1[1499].date_active


        else:
            objs = Account.objects.filter(date_active__gt=d[3].date_active).count()
            if objs <= 1500:
                team += objs
                try:
                    d1 = d[4].date_active
                except Exception as e:
                    pass
            else:
                team += 1500
                obj1  = obj.objects.filter(date_active__gt=d[3].date_active).order_by('date_active')
                d1 = obj1[299].date_active

    if direct >= 5:
        if d[4].date_active <= d1:
            objs = Account.objects.filter(date_active__gt=d1).count()
            if objs <= 3500:
                team += objs
                try:
                    d1 = d[5].date_active
                except Exception as e:
                    pass
            else:
                team += 3500
                obj1  = obj.objects.filter(date_active__gt=d1).order_by('date_active')
                d1 = obj1[3499].date_active


        else:
            objs = Account.objects.filter(date_active__gt=d[2].date_active).count()
            if objs <= 3500:
                team += objs
                try:
                    d1 = d[5].date_active
                except Exception as e:
                    pass
            else:
                team += 3500
                obj1  = obj.objects.filter(date_active__gt=d[2].date_active).order_by('date_active')
                d1 = obj1[3499].date_active


    if direct >= 6:
        if d[5].date_active <= d1:
            objs = Account.objects.filter(date_active__gt=d1).count()
            if objs <= 25000:
                team += objs
                try:
                    d1 = d[6].date_active
                except Exception as e:
                    pass
            else:
                team += 25000
                obj1  = obj.objects.filter(date_active__gt=d1).order_by('date_active')
                d1 = obj1[2499].date_active


        else:
            objs = Account.objects.filter(date_active__gt=d[6].date_active).count()
            if objs <= 25000:
                team += objs
                try:
                    d1 = d[6].date_active
                except Exception as e:
                    pass
            else:
                team += 25000
                obj1  = obj.objects.filter(date_active__gt=d[6].date_active).order_by('date_active')
                d1 = obj1[2499].date_active

    if direct >= 7:
        if d[6].date_active <= d1:
            objs = Account.objects.filter(date_active__gt=d1).count()
            if objs <= 50000:
                team += objs
                try:
                    d1 = d[7].date_active
                except Exception as e:
                    pass
            else:
                team += 50000
                obj1  = obj.objects.filter(date_active__gt=d1).order_by('date_active')
                d1 = obj1[49999].date_active


        else:
            objs = Account.objects.filter(date_active__gt=d[6].date_active).count()
            if objs <= 800:
                team += objs
                try:
                    d1 = d[7].date_active
                except Exception as e:
                    pass
            else:
                team += 800
                obj1  = obj.objects.filter(date_active__gt=d[6].date_active).order_by('date_active')
                d1 = obj1[299].date_active

    if direct >= 8:
        if d[7].date_active < d1:
            objs = Account.objects.filter(date_active__gt=d1).count()
            if objs <= 100000:
                team += objs
            else:
                team += 100000
                obj1  = obj.objects.filter(date_active__gt=d1).order_by('date_active')
                d1 = obj1[99999].date_active


        else:
            objs = Account.objects.filter(date_active__gt=d[7].date_active).count()
            if objs <= 100000:
                team += objs
            else:

                obj1  = obj.objects.filter(date_active__gt=d[7].date_active).order_by('date_active')
                team += obj1.count() + 1


'''
