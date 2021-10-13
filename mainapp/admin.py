from django.contrib import admin
from .models import UserAuthentication, ForgetPass

admin.site.register(UserAuthentication)
admin.site.register(ForgetPass)