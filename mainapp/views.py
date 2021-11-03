from django.http import request
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from .tasks import bbot
from .models import UserAuthentication, User, ForgetPass, Pre_User, VerifyMe
from .helpers import mail_for_pass, welcome_mail, contact_us_mail
import uuid

def Home(request):

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True

    return render(request, 'index.html', {'userp':userp})

def tac(request):

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True

    return render(request, 'tac.html', {'userp':userp})

def pp(request):

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True
        
    return render(request, 'pp.html', {'userp':userp})

def dis(request):

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True

    return render(request, 'dis.html', {'userp':userp})

def register(request):

    userp = True

    if request.method == 'POST':

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        conpass = request.POST.get('password2')

        if username == '':
            messages.error(request, 'You must enter Username')
            return redirect('register')

        elif email == '':
            messages.error(request, 'You must enter Email')
            return redirect('register')

        elif password == '':
            messages.error(request, 'You must enter Password')
            return redirect('register')

        elif conpass == '':
            messages.error(request, 'You must enter Confirm Password')
            return redirect('register')

        elif password != conpass:
            messages.error(request, 'Confirm Password And Password Must Be Same')
            return redirect('register')

        elif User.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('register')

        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already Taken')
            return redirect('register')

        else:
            user_obj = User(username=username, email=email)
            user_obj.set_password(password)
            user_obj.save()

            htmly = get_template('registration/email.html')
            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())

            forgetpass_obj = VerifyMe.objects.update_or_create(
                U_User = user_obj,
                defaults = {
                    "V_B_TO": token,
                }
            )

            welcome_mail(username, email, htmly, token)
            messages.success(request, f'Your account has been created ! Check your mail to verify !!')

            return redirect('login')

    return render(request, 'registration/register.html', {'userp':userp})

def Login(request):

    userp = True

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username=username).first()
        user_obj = VerifyMe.objects.filter(U_User=user).first()

        if username == '':
            messages.error(request, 'You must enter Username')
            return redirect('login')

        elif password == '':
            messages.error(request, 'You must enter Password')
            return redirect('login')

        elif User.objects.filter(username=username).exists() == False:
            messages.warning(request, 'account does not exit plz sign in')
            return redirect('login')

        elif user_obj.V_B_TO != user_obj.V_A_TO:
            messages.warning(request, 'First Verify your account to Login')
            return redirect('login')

        elif username != '' and password != '':
            user_obj = authenticate(request, username = username, password = password)

            if user_obj is None:
                messages.warning(request, 'Worng Password Try Again')
                return redirect('login')

            login(request, user_obj)
            messages.success(request, f' welcome {username} !!')

            if UserAuthentication.objects.filter(U_User=request.user).exists() == False:
                return redirect('UserAuthForm')

            return redirect('Home')

    return render(request, 'registration/login.html', {'userp':userp})

def Logout(request):
    logout(request)
    return redirect('Home')

@login_required(login_url='login')
def UserAuthform(request):

    userp = True

    if request.method == 'POST':

        user = request.user.username
        auth = request.POST.get('D_Auth')
        chid = request.POST.get('D_ChID')
        utyp = request.POST.get('U_Type')
        loss = request.POST.get('N_Loss')

        if auth == '':
            messages.error(request, 'Authentication Key Must be Entered')
            return redirect('UserAuthForm')

        elif chid == '':
            messages.error(request, 'Channel ID Must be Entered')
            return redirect('UserAuthForm')

        elif UserAuthentication.objects.filter(D_Auth=auth).exists():
            messages.warning(request, 'Authentication key in Use')
            return redirect('UserAuthForm')

        elif utyp == '':
            messages.error(request, 'User Type Must Be Selected')
            return redirect('UserAuthForm')

        else:
            user_obj = User.objects.get(username=user)

            userauth_obj = UserAuthentication.objects.update_or_create(
                U_User = user_obj,
                defaults = {
                    "D_Auth": auth,
                    "D_ChID": chid,
                    "U_Type": utyp,
                    "N_Loss": loss,
                }
            )

            messages.success(request, 'Now you can start your bot in BOT page')

            return redirect('Home')

    return render(request, 'registration/userauthform.html', {'userp':userp})

@login_required(login_url='login')
def UserAuthemail(request):

    userp = True

    if request.method == 'POST':

        user = request.user
        email = request.POST.get('Email')
        passw = request.POST.get('password')
        chid = request.POST.get('D_ChID')
        utyp = request.POST.get('U_Type')
        loss = request.POST.get('N_Loss')

        if email == '':
            messages.error(request, 'Email Must be Entered')
            return redirect('UserAuthEmail')

        elif passw == '':
            messages.error(request, 'Password ID Must be Entered')
            return redirect('UserAuthEmail')

        elif chid == '':
            messages.error(request, 'Channel ID Must be Entered')
            return redirect('UserAuthEmail')

        elif UserAuthentication.objects.filter(E_Mail=email).exists():
            messages.warning(request, 'Email is already in use')
            return redirect('UserAuthEmail')

        elif utyp == '':
            messages.error(request, 'User Type Must Be Selected')
            return redirect('UserAuthEmail')

        else:
            user_obj = User.objects.get(username=user)

            userauth_obj = UserAuthentication.objects.update_or_create(
                U_User = user_obj,
                defaults = {
                    "E_Mail": email,
                    "P_Word": passw,
                    "D_ChID": chid,
                    "U_Type": utyp,
                    "N_Loss": loss,
                }
            )

            messages.success(request, 'Now you can start your bot in BOT page')

            return redirect('Home')

    return render(request, 'registration/userauthemail.html', {'userp':userp})

def EditProfile(request):
    user = request.user
    userauth = UserAuthentication.objects.get(U_User=user)

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True

    if request.method == 'POST':

        usern = request.POST.get('username')     
        email = request.POST.get('id_email')
        chid = request.POST.get('D_ChID')
        dnme = request.POST.get('Email')
        dpas = request.POST.get('password')
        utyp = request.POST.get('U_Type')
        loss = request.POST.get('N_Loss')

        if usern != user.username:
            if User.objects.filter(username=usern).exists():
                messages.warning(request, 'Username is already taken')
                return redirect('edit_profile')

        elif user.email != email:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email is already Taken')
                return redirect('edit_profile')

        elif userauth.E_Mail != dnme:
            if UserAuthentication.objects.filter(E_Mail=dnme).exists():
                messages.warning(request, 'Email ID is already in use')
                return redirect('edit_profile')

        if True:
            userauth_obj = UserAuthentication.objects.update_or_create(
                U_User = user,
                defaults = {
                    "D_ChID": chid,
                    "U_Type": utyp,
                    "N_Loss": loss,
                    "E_Mail": dnme,
                    "P_Word": dpas,
                }
            )
            user_obj = User.objects.update_or_create(
                username = user.username,
                defaults = {
                "username": usern,
                "email": email,
                }
            )
            messages.success(request, 'Update successfull')
            return redirect('Home')

    return render(request, 'registration/edit_profile.html', {'user': user, 'userauth': userauth, 'userp':userp})

def ChangePass(request, token):
    context = {}

    forgetpass_obj = ForgetPass.objects.filter(F_P_TO = token).first()
    context = {'username': forgetpass_obj.U_User.username}

    userp = True

    if request.method == 'POST':
        new_pass = request.POST.get('new_password')
        con_pass = request.POST.get('confirm_password')
        username = request.POST.get('username')

        if username is None:
            messages.warning(request, "No user found")
            return redirect(f'/changepass/{token}/')

        if new_pass != con_pass:
            messages.error(request, "New Password And Confirm Password Must Be Same")
            return redirect(f'/changepass/{token}/')

        user_obj = User.objects.get(username = username)
        user_obj.set_password(new_pass)
        user_obj.save()

        messages.success(request, 'Password changed successfully')

        return redirect('login')

    return render(request, 'registration/changepass.html', {'context':context, 'userp':userp})

def Forgetpass(request):

    userp = True

    if request.method == 'POST':
        user = request.POST.get('username')

        if not User.objects.filter(username=user).exists():
            messages.warning(request, 'No user found with user username')
            return redirect('forgetpass')

        user_obj = User.objects.get(username=user)
        token = str(uuid.uuid4())

        forgetpass_obj = ForgetPass.objects.update_or_create(
            U_User = user_obj,
            defaults = {
                "F_P_TO": token,
            }
        )

        mail_for_pass(user_obj.email, token)
        messages.info(request, 'Check your Email Inbox')
        return redirect('forgetpass')

    return render(request, 'registration/forgetpass.html', {'userp':userp})

def VerifyEmail(request, token):

    user_obj = VerifyMe.objects.filter(V_B_TO=token).first()

    user_ver = VerifyMe.objects.update_or_create(
        U_User = user_obj.U_User,
        defaults = {
            "V_A_TO": token,
        }
    )

    messages.success(request, 'Check your Email Inbox')
    return redirect('login')

def AboutUs(request):

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True

    return render(request, 'about.html', {'userp':userp})

def ContactUs(request):

    userp = True

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        contact_us_mail(name, email, subject, message)
        messages.success(request, "Your ticket created successfully we will reach you as soon as possible")
        return redirect('contactus')

    return render(request, 'contact.html', {'userp':userp})

def Donate(request):

    userp = True

    return render(request, 'donate.html', {'userp':userp})

def Bot(request):

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True

    return render(request, 'selfbot.html', {'userp':userp})

def TypeBot(request, pk):
    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True
    try:
        user_obj = request.user.username
        bbot.delay(pk, user_obj)
        messages.success(request, f"Your {pk} Bot Starts Come Again After 2 Hours")
        return redirect('bot')
    except ValueError as e:
        print(e)

def Pmembership(request):

    userp = True

    return render(request, 'pricing.html', {'userp':userp})

def AuthHelp(request):

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True

    return render(request, 'auth_help.html', {'userp':userp})

def Error_404(request, exception):

    if request.user.is_authenticated:
        userp = Pre_User.objects.filter(U_User=request.user).exists
    else:
        userp = True

    return render(request, '404.html', {'userp':userp})