from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from api.models import Student, Event

# Create your views here.
def event_create(request):
	if request.method == "POST":
		student_id = request.POST.get("student_id", "")
		longitude = request.POST.get("longitude", "")
		latitude = request.POST.get("latitude", "")
		scanner_name = request.POST.get("scanner_name", "")

		student = Student.objects.get(id=student_id)

		try:
			event = Event(
				student=student,
				longitude=float(longitude),
				latitude=float(latitude),
				scanner_name=scanner_name
			)
			event.save()

			return JsonResponse({
				"status": "success",
				"message": None,
				"data": event.id
			})
		except:
			return JsonResponse({
				"status": "error",
				"message": "bro, something broke in the create event API endpoint",
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
