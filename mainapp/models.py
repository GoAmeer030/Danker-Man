from django.db import models
from django.contrib.auth.models import User

class UserAuthentication(models.Model):
    U_User = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key= True,
    )

    D_Auth = models.CharField(max_length=100, unique=True)
    D_ChID = models.CharField(max_length=100, unique=True)
    U_Type = models.CharField(max_length=7)
    N_Loss = models.CharField(max_length=7)
    U_PreM = models.BooleanField(null=False, default=False)
    U_Agen = models.CharField(max_length=250, null=True)
    B_Numb = models.PositiveIntegerField(null=True)

    def __str__(self):
        return self.U_User.username

class ForgetPass(models.Model):
    U_User = models.OneToOneField(
        User,
        on_delete=models.CASCADE
        )

    F_P_TO = models.CharField(max_length=100)
    F_Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.U_User.username
