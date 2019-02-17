from django.shortcuts import render
from rest_framework import generics
from .models import Locker, Log
from .serializers import LockerSerializer, LogSerializer
