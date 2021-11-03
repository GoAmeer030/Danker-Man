from django.contrib import admin
from .models import UserAuthentication, ForgetPass, Pre_User, VerifyMe

admin.site.register(UserAuthentication)
admin.site.register(ForgetPass)
admin.site.register(Pre_User)
admin.site.register(VerifyMe)