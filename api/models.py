from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import qrcode
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

# Create your models here.
class Student(models.Model):
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)

	notifications = models.BooleanField(default=False)

	parent = models.ForeignKey(User, on_delete=models.CASCADE)
	
	qr_code = models.ImageField(upload_to='qrcodes', blank=True, null=True)

	def generate_qrcode(self):
		qr = qrcode.QRCode(
		    version=1,
		    error_correction=qrcode.constants.ERROR_CORRECT_L,
		    box_size=6,
		    border=0,
		)
		qr.add_data(self.id)
		qr.make(fit=True)

		img = qr.make_image()

		buffer = io.BytesIO()
		img.save(buffer)
		filename = 'student-%s.png' % (self.id)
		filebuffer = InMemoryUploadedFile(
			buffer, None, filename, 'image/png', sys.getsizeof(buffer), None)
		self.qr_code.save(filename, filebuffer)

class Event(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	
	latitude = models.DecimalField(max_digits=9, decimal_places=6)
	longitude = models.DecimalField(max_digits=9, decimal_places=6)

	scanner_name = models.TextField()

	time = models.DateTimeField(auto_now_add=True)
