from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Locker, Log
from .serializers import LockerSerializer, LogSerializer


class AllLockers(APIView):

	def get(self, request, format=None):
		lockers = Locker.objects.all()
		serializer = LockerSerializer(lockers, many=True)
		return Response(serializer.data)


class CameraView(APIView):

	def get(self, request, locker_id, format=None):
		logs = Log.objects.filter(locker__pk=locker_id)
		serializer = LogSerializer(logs, many=True)
		return Response(serializer.data)

	def post(self, request, locker_id, format=None):
		serializer = LogSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusView(APIView):

	def get_object(self, locker_id):
		try:
			return Locker.objects.get(pk=locker_id)
		except Locker.DoesNotExist:
			raise Http404

	def get(self, request, locker_id, format=None):
		locker = self.get_object(locker_id)
		serializer = LockerSerializer(locker)
		return Response(serializer.data['open_status'])

	def put(self, request, locker_id, format=None):
		locker = self.get_object(locker_id)
		serializer = LockerSerializer(locker, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OpenView(APIView):

	def get_object(self, locker_id):
		try:
			return Locker.objects.get(pk=locker_id)
		except Locker.DoesNotExist:
			raise Http404

	def get(self, request, locker_id, format=None):
		locker = self.get_object(locker_id)
		serializer = LockerSerializer(locker)
		return Response(serializer.data['accessible'])

	def put(self, request, locker_id, format=None):
		locker = self.get_object(locker_id)
		serializer = LockerSerializer(locker, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
