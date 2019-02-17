from django.urls import path
from . import views


urlpatterns = [
	path('locker/<int:locker_id>/camera', views.CameraView),
	path('locker/<int:locker_id>/status', views.StatusView),
	path('locker/<int:locker_id>/open', views.OpenView),
]