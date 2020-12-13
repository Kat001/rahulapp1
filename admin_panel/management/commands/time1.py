from django.core.management.base import BaseCommand
from django.utils import timezone
from profile_app.models import Update_Roi_Income,All_Roi_Income
from Accounts.models import Account

class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        objs = Update_Roi_Income.objects.all()
        for obj in objs:
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
        print("Done!!!!!")
