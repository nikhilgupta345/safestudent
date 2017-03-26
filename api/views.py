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
