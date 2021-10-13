from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def mail_for_pass(email, token):
	subject = "Reset Password"
	message = f'Click the link to change your password http://127.0.0.1:8000/reset_pass/{token}/'
	email_from = settings.EMAIL_HOST_USER
	send_mail(subject, message, email_from, [email])
	return 1

def welcome_mail(username, email, htmly):
	d = { 'username': username }
	subject = 'Welcome'
	from_email = 'dankerman.cservice@gmail.com'
	to = email
	html_content = htmly.render(d)
	msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
	msg.attach_alternative(html_content, "text/html")
	msg.send()

def contact_us_mail(name, email, subject, message):
	message = f'{name} {email} {message}'
	email_from = settings.EMAIL_HOST_USER
	send_mail(subject, message, email_from, ['dankerman.cservice@gmail.com'])
	return 1