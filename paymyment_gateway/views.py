from django.shortcuts import render,redirect
import razorpay
from .models import Payment_Fund
from django.views.decorators.csrf import csrf_exempt
from profile_app.models import *
from Accounts.models import Account

# Create your views here.
@csrf_exempt
def payment(request):
    user = request.user
    user_obj = Account.objects.get(username = user.username)

    if request.method == 'POST':
        name = request.POST.get('name')
        amount = int(request.POST.get('amount')) * 100

        client = razorpay.Client(auth= ('rzp_live_PVwIqdcl5fd42V','RtnHu5Fi5pa53bU7EWsV6aIV'))
        payment = client.order.create({'amount':amount, 'currency':'INR','payment_capture':'1' })
        print(payment)
        obj = Payment_Fund(name=name,amount=amount,order_id=payment['id'])
        obj.save()
        return render(request,'payment.html',{'payment':payment})


    return render(request,'payment.html',{'user':user})

def success(request):
    if request.method == 'POST':
        a = request.POST
        print(a)
    return render(request,'success.html')
