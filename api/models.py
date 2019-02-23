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
	open_time = models.DateTimeField(default=timezone.now)
	close_time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return str(self.locker.pk) + ' - ' + str(self.pk)
