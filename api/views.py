from django.http import Http404
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
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


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=status.HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=status.HTTP_200_OK)
