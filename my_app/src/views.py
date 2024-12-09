from django.http import HttpResponse
from django.template import loader

def login_view(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())

def register_view(request):
  template = loader.get_template('register.html')
  return HttpResponse(template.render())


def dashboard_view(request):
  template = loader.get_template('dashboard.html')
  return HttpResponse(template.render())

def overall_view(request):
  template = loader.get_template('overall.html')
  return HttpResponse(template.render())

def modelling_view(request):
  template = loader.get_template('modelling.html')
  return HttpResponse(template.render())