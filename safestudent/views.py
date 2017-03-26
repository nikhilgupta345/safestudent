from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from api.models import Student, Event

# LOGIN
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
				'message': "Either that username or password was wrong. Try again?"
			})
	elif request.user.is_authenticated():
		return HttpResponseRedirect('/')
		
	return render(request, 'login.html')

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login')

def register(request):
	if request.user.is_authenticated():
		return HttpResponse('/login')

	elif request.method == "GET":
		return render(request, 'register.html')

	firstname = request.POST.get('firstname', '').strip()
	lastname = request.POST.get('lastname', '').strip()
	email = request.POST.get('email', '').strip()
	username = request.POST.get('username', '').strip()
	password = request.POST.get('password', '')
	confirm = request.POST.get('confirm-password', '')

	if len(firstname) < 2 or len(lastname) < 2:
		return render(request, 'register.html', {
			'message': "Your name wasn't valid."
		})
	if username == "":
		return render(request, 'register.html', {
			'message': "Your username was empty."
		})
	if password != confirm:
		return render(request, 'register.html', {
			'message': "Your passwords didn't match."
		})
	if len(User.objects.filter(username=username)) != 0:
		return render(request, 'register.html', {
			'message': "That username already exists."
		})
	try:
		auth.password_validation.validate_password(password, settings.AUTH_PASSWORD_VALIDATORS)
	except ValidationError as e:
		return render(request, 'register.html', {
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


# PAGES
@login_required
def index(request):
	if request.user.is_staff:
		students = Student.objects.all()
		response = []
		for student in students:
			try:
				event = Event.objects.filter(student=student).order_by("-time")[0]
				response.append({
					"id": student.id,
					"name": student.first_name + " " + student.last_name,
					"last": event.scanner_name,
					"time": event.time
				})
			except:
				response.append({
					"id": student.id,
					"name": student.first_name + " " + student.last_name,
					"last": "",
					"time": ""
				})
		parents = User.objects.filter(is_staff=False)
		
		return render(request, 'index-staff.html', {
			"students": response,
			"parents": parents
		})
	else:
		students = request.user.student_set.all()
		response = []
		for student in students:
			try:
				event = Event.objects.filter(student=student).order_by("-time")[0]
				response.append({
					"id": student.id,
					"name": student.first_name + " " + student.last_name,
					"last": event.scanner_name,
					"time": event.time
				})
			except:
				response.append({
					"id": student.id,
					"name": student.first_name + " " + student.last_name,
					"last": "",
					"time": ""
				})

		return render(request, 'index.html', {
			"students": response
		})

def student_register(request):
	if request.method == "POST":
		first_name = request.POST.get('first-name', "")
		last_name = request.POST.get('last-name', "")
		parent_option = request.POST.get('parent-option', "")

		parent = User.objects.get(id=parent_option)

		s = Student(
			first_name=first_name,
			last_name=last_name,
			parent=parent
		)
		s.save()
		s.generate_qrcode()
		
	return HttpResponseRedirect('/')

def student_profile(request, student_id):
	# Check if staff or parent of user
	student = Student.objects.get(id=student_id)
	parent = student.parent
	if request.user.is_staff or request.user == parent:
		events = []
		for event in student.event_set.all().order_by('-time'):
			events.append({
				"scanner_name": event.scanner_name,
				"longitude": event.longitude,
				"latitude": event.latitude,
				"time": event.time
			})

		return render(request, 'student.html', {
			"student": student,
			"events": events
		})
	else:
		return render(request, 'error.html', {})

def student_notifications_on(request, student_id):
	# Check if staff or parent of user
	student = Student.objects.get(id=student_id)
	student.notifications = True
	student.save()
	return HttpResponseRedirect('/student/' + student_id)

def student_notifications_off(request, student_id):
	# Check if staff or parent of user
	student = Student.objects.get(id=student_id)
	student.notifications = False
	student.save()
	return HttpResponseRedirect('/student/' + student_id)

def feed(request):
	if request.user.is_staff:
		events = Event.objects.all().order_by("-time")
		response = []
		for event in events:
			response.append({
				"student_first_name": event.student.first_name,
				"student_last_name": event.student.last_name,
				"scanner_name": event.scanner_name,
				"time": event.time
			})
		return render(request, 'feed.html', {
			"events": response
		})
	return render(request, 'error.html', {})