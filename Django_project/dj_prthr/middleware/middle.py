#encoding:utf-8
from django.http.response import HttpResponse

class selfmiddleware(object):
  def process_request(self, request):
    print "1 Process request"

  def process_view(self, request, callback, callback_args, callback_kwargs):
    print "1 process view"

  def process_exception(self, request, exception):
    print "1 process exception"

  def process_response(self, request, response):
    print "1 process response"
    return response
