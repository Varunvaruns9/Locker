from django.http import Http404, HttpResponse
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Locker, Log, Pin
from .serializers import LockerSerializer, LogSerializer
import dropbox

access_token = 'emeqlLb3TSgAAAAAAAAAIsroEFyj__gpE8g1JP_X9lDvZ0E6f8dOwnyigwPkPQw5'


class AllLockers(APIView):

	def get(self, request, format=None):
		lockers = Locker.objects.all()
		serializer = LockerSerializer(lockers, many=True)
		return Response(serializer.data)


class LogView(APIView):

	def get(self, request, locker_id, format=None):
		logs = Log.objects.filter(locker__pk=locker_id)
		serializer = LogSerializer(logs, many=True)
		return Response(serializer.data)

	def post(self, request, locker_id, format=None):
		serializer = LogSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			# dbx = dropbox.Dropbox(access_token)
			# path = '/locker' + str(locker_id) + '/' + str(serializer.data['id']) + '.mp4'
			# dbx.files_upload(request.FILES['file'].read(), path)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LockerDetailsView(APIView):

	def get_object(self, locker_id):
		try:
			return Locker.objects.get(pk=locker_id)
		except Locker.DoesNotExist:
			raise Http404

	def get(self, request, locker_id, format=None):
		locker = self.get_object(locker_id)
		serializer = LockerSerializer(locker)
		return Response(serializer.data)

	def patch(self, request, locker_id, format=None):
		locker = self.get_object(locker_id)
		if "accessible" in request.data and request.data["accessible"]:
			random = get_random_string(length=32)
			pin = Pin(pin=random, locker=locker)
			print(random)
			pin.save()
			send_mail(
					    'Locker %d access verification.' % locker_id,
					    'Please use this url to verify the locker access request for the locker: http://lockerapi.herokuapp.com/api/locker/' + random,
					    settings.EMAIL_HOST_USER,
					    [request.user.email, ],
					    fail_silently=False,
					)
			return Response({'status': 'Check your email'})
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


@csrf_exempt
def open(request, token):
	pin = Pin.objects.get(pin=token)
	print(pin)
	if pin is None or token == '':
		raise Http404
	locker = pin.locker
	locker.accessible = True
	locker.save()
	html = "Hey, success."
	return HttpResponse(html)
