from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from api.models import Student, Event
import os
import sendgrid
from sendgrid.helpers.mail import *

# Create your views here.
def event_create(request):
	if request.method == "POST":
		uuid = request.POST.get("uuid", "")
		longitude = request.POST.get("longitude", "")
		latitude = request.POST.get("latitude", "")
		scanner_name = request.POST.get("scanner_name", "")

		try:
			student = Student.objects.get(uuid=int(uuid))
		except:
			return JsonResponse({
				"status": "error",
				"message": "No student with that uuid",
				"data": None
			})

		try:
			event = Event(
				student=student,
				longitude=float(longitude),
				latitude=float(latitude),
				scanner_name=scanner_name
			)
			event.save()

			# Send email if notifications turned on
			if student.notifications:
				parent_email = student.parent.email
				subject_text = student.first_name + " checked into " + event.scanner_name + " just now"
				content_text = "This is just a friendly notification - please use your account to see more detailed information. Thanks for using SafeStudent!"

				sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))

				from_email = Email("noreply@safestudent.com")
				to_email = Email(parent_email)
				subject = subject_text
				content = Content("text/plain", content_text)
				mail = Mail(from_email, subject, to_email, content)
				response = sg.client.mail.send.post(request_body=mail.get())

			return JsonResponse({
				"status": "success",
				"message": None,
				"data": event.id
			})
		except Exception as e:
			return JsonResponse({
				"status": "error",
				"message": str(e),
				"data": None
			})
	return JsonResponse({
		"status": "error",
		"message": "dude it needs to be a post request",
		"data": None
	})

def event_delete(request):
	if request.method == "POST":
		event_id = request.POST.get("event_id")

		try:
			event = Event.objects.get(id=event_id)
			event.delete()
		except:
			return JsonResponse({
				"status": "error",
				"message": "idk something broke in the delete event API endpoint",
				"data": None
			})
	return JsonResponse({
		"status": "error",
		"message": "told you it needs to be a post",
		"data": None
	})

def event_all(request):
	events = Event.objects.all()
	response = []
	for event in events:
		response.append({
			"event_id": event.id,
			"student_first_name": event.student.first_name,
			"student_last_name": event.student.last_name,
			"scanner_name": event.scanner_name,
			"time": event.time
		})
	return JsonResponse({
		"status": "success",
		"message": None,
		"data": response
	})

def get_student_info(request):
	data = {
		"students": []
	}

	if 'student_id' in request.GET:
		try:
			if request.user.is_staff:
				students = Student.objects.filter(id=int(request.GET.get('student_id', '')))
			else:
				students = request.user.student_set.filter(id=int(request.GET.get('student_id', '')))
		except:
			return JsonResponse({
				"status": "error",
				"message": "Invalid student ID provided.",
				"data": None
			})
	else:
		if request.user.is_staff:
			students = Student.objects.all()
		else:
			students = request.user.student_set.all()

	for student in students:
		student_info = {
			"name": student.first_name + " " + student.last_name
		}
		events = []
		for event in student.event_set.all().order_by('time'):
			events.append({
				"latitude": event.latitude,
				"longitude": event.longitude,
				"name": event.scanner_name,
				"timestamp": event.time
			})

		student_info["events"] = events
		data["students"].append(student_info)

	return JsonResponse({
		"status": "success",
		"message": None,
		"data": data
	})
