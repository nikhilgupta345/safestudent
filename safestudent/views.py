from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

@login_required
def index(request):
	students = request.user.student_set.all()
	return render(request, 'index.html', {
		"students": students
	})

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		# Log user in and save time
		if user is not None:
			auth.login(request, user)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'login.html', {
				'login_message': "Either that username or password was wrong. Try again?"
			})
	elif request.user.is_authenticated():
		return HttpResponseRedirect('/')
		
	return render(request, 'login.html')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login')

def register(request):
	if request.method != "POST" or request.user.is_authenticated():
		return HttpResponseRedirect('/login')

	firstname = request.POST.get('firstname', '').strip()
	lastname = request.POST.get('lastname', '').strip()
	email = request.POST.get('email', '').strip()
	username = request.POST.get('username', '').strip()
	password = request.POST.get('password', '')
	confirm = request.POST.get('confirm-password', '')

	if len(firstname) < 2 or len(lastname) < 2:
		return render(request, 'login.html', {
			'register_message': "Your name wasn't valid."
		})
	if username == "":
		return render(request, 'login.html', {
			'register_message': "Your username was empty."
		})
	if password != confirm:
		return render(request, 'login.html', {
			'register_message': "Your passwords didn't match."
		})
	if len(User.objects.filter(username=username)) != 0:
		return render(request, 'login.html', {
			'register_message': "That username already exists."
		})
	try:
		auth.password_validation.validate_password(password, settings.AUTH_PASSWORD_VALIDATORS)
	except ValidationError as e:
		return render(request, 'login.html', {
			'validations': e
		})
		
	user = User.objects.create_user(
		first_name=firstname,
		last_name=lastname,
		email=email,
		username=username,
		password=password
	)

	auth.login(request, user)
	return HttpResponseRedirect('/')