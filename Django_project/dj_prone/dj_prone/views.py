#encoding:utf-8
from django.shortcuts import render
from django.http.response import HttpResponse

def index(request):
  return HttpResponse('Hello Django')

def login(request):
  return HttpResponse('Login')

def register(request):
  return HttpResponse('Register')

def list(request, item, id):
  num = int(id)
  return HttpResponse(num)

