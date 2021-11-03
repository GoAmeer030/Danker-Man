from django.db import models
from django.contrib.auth.models import User

class UserAuthentication(models.Model):
    U_User = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key= True,
    )

    D_Auth = models.CharField(max_length=100, null=True)
    E_Mail = models.EmailField(max_length=100, null=True)
    P_Word = models.CharField(max_length=100, null=True)
    D_ChID = models.CharField(max_length=100)
    U_Type = models.CharField(max_length=7)
    N_Loss = models.CharField(max_length=7)
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


class Pre_User(models.Model):
    U_User = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    P_User = models.CharField(max_length=9)

    def __str__(self):
        return self.U_User.username

class VerifyMe(models.Model):
    U_User = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    V_B_TO = models.CharField(max_length=100)
    V_A_TO = models.CharField(max_length=100)
    F_Date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.U_User.username
