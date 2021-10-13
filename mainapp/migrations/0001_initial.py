# Generated by Django 3.2.7 on 2021-10-13 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAuthentication',
            fields=[
                ('U_User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='auth.user')),
                ('D_Auth', models.CharField(max_length=100, unique=True)),
                ('D_ChID', models.PositiveIntegerField()),
                ('U_Type', models.CharField(max_length=7)),
                ('N_Loss', models.CharField(max_length=7)),
                ('U_PreM', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ForgetPass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('F_P_TO', models.CharField(max_length=100)),
                ('F_Date', models.DateTimeField(auto_now_add=True)),
                ('U_User', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
