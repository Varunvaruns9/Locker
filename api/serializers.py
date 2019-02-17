from rest_framework import serializers
from .models import Locker, Log


class LockerSerializer(serializers.ModelSerializer):
	class Meta:
		model = Locker
		fields = ('__all__')


class LogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Log
		fields = ('__all__')
