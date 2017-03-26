from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)

	parent = models.ForeignKey(User, on_delete=models.CASCADE)
	
	qr_code = models.ImageField(upload_to='qrcodes', blank=True, null=True)

class Event(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)

	scanner_name = models.TextField()

	time = models.DateTimeField(auto_now_add=True)
