from django.shortcuts import render_to_response
from django.contrib.auth.forms import UserCreationForm 

def registration(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
    
    context = {'form' : form}

    return render_to_response('registration.html', context)
