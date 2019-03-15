from django.db import models
from django.utils import timezone

# Create your models here.
class Locker(models.Model):
	# True indicates locker is currently open
	open_status = models.BooleanField(default=False)
	# True indicates locker is accessible
	accessible = models.BooleanField(default=False)

	def __str__(self):
		return str(self.pk)


class Log(models.Model):
	locker = models.ForeignKey('Locker', on_delete=models.CASCADE)
	open_time = models.CharField(max_length=100)
	close_time = models.CharField(max_length=100)

	def __str__(self):
		return str(self.locker.pk) + ' - ' + str(self.pk)


class Pin(models.Model):
	pin = models.CharField(max_length=32, null=True, blank=True)
	locker = models.ForeignKey(Locker, on_delete=models.CASCADE)