# Generated by Django 3.0.8 on 2020-11-22 17:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(blank=True, max_length=60, null=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('date_active', models.DateTimeField(default='2000-01-01 06:00', verbose_name='date active')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_active1', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('down_team', models.IntegerField(blank=True, default=0, null=True)),
                ('total_team', models.TextField(blank=True, max_length=10000000, null=True)),
                ('total_rank_income', models.FloatField(default=0)),
                ('total_level_income', models.FloatField(default=0)),
                ('total_roi_income', models.FloatField(default=0)),
                ('total_direct_income', models.FloatField(default=0)),
                ('refund', models.FloatField(default=0)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('sponser', models.CharField(blank=True, max_length=30, null=True)),
                ('upline', models.CharField(blank=True, max_length=30, null=True)),
                ('downline', models.CharField(blank=True, max_length=30, null=True)),
                ('txn_password', models.CharField(max_length=30)),
                ('phon_no', models.CharField(blank=True, max_length=12, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True, verbose_name='date of birth')),
                ('state', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('zip', models.CharField(blank=True, max_length=6, null=True)),
                ('image', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='profile_pics')),
                ('rem_paas', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='All_Withrawal_Request1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('account_holder_name', models.CharField(default='', max_length=40)),
                ('account_number', models.CharField(default='', max_length=30)),
                ('branch_name', models.CharField(default='', max_length=40)),
                ('ifsc_code', models.CharField(default='', max_length=20)),
                ('bank_name', models.CharField(default='', max_length=30)),
                ('status', models.CharField(default='', max_length=30)),
                ('amount', models.FloatField(default=0)),
                ('charge', models.FloatField(default=0)),
                ('w_amount', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='All_Withrawal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('account_holder_name', models.CharField(default='', max_length=40)),
                ('account_number', models.CharField(default='', max_length=30)),
                ('branch_name', models.CharField(default='', max_length=40)),
                ('ifsc_code', models.CharField(default='', max_length=20)),
                ('bank_name', models.CharField(default='', max_length=30)),
                ('status', models.CharField(default='', max_length=30)),
                ('amount', models.FloatField(default=0)),
                ('charge', models.FloatField(default=0)),
                ('w_amount', models.FloatField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
