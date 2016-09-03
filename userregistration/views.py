from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import ContributorCreationForm
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

def registration(request):
    csrf_token = {}
    csrf_token.update(csrf(request))

    form = ContributorCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        return HttpResponseRedirect('/thanks/')

    context = {'form' : form}
#TODO
    return render(request, 'registration.html', context)
