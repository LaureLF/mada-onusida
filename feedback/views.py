from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from feedback.forms import FeedbackForm
#from django.template.context_processors import csrf

def submit_bug(request):
  # Use CSRF tokens
#  c = {}
#  c.update(csrf(request))
  # if the request is a POST request
  if request.method == 'POST':
    form = FeedbackForm(request.POST)
    if form.is_valid():
      form.save()
#      return render(c, "feedback/merci.html")
      return HttpResponseRedirect('/bugs/merci')

  # if the request is a GET request
  else:
    form = FeedbackForm()
  return render(request, "feedback/submit.html", { 'form' : form })

def merci(request):
    template = loader.get_template('feedback/merci.html')
    return HttpResponse(template.render())
