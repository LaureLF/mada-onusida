from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render
from feedback.forms import FeedbackForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='/admin/login')
def submit_bug(request):
  # if the request is a POST request
  if request.method == 'POST':
    form = FeedbackForm(request.POST)
    if form.is_valid():
      form.save()
      return HttpResponseRedirect('/bugs/merci')

  # if the request is a GET request
  else:
    form = FeedbackForm()
  return render(request, "feedback/submit.html", { 'form' : form })

def merci(request):
    template = loader.get_template('feedback/merci.html')
    return HttpResponse(template.render())
