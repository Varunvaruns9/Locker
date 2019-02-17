from django.urls import path
from . import views


urlpatterns = [
	path('login', views.login),
	path('locker', views.AllLockers.as_view()),
	path('locker/<int:locker_id>/camera', views.CameraView.as_view()),
	path('locker/<int:locker_id>/status', views.StatusView.as_view()),
	path('locker/<int:locker_id>/open', views.OpenView.as_view()),
]