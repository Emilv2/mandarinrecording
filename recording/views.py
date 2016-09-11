from django.shortcuts import render
from django.template.context_processors import csrf

def recording(request):
    csrf_token = {}
    csrf_token.update(csrf(request))
    context = {}

    return render(request, 'recording.html', context)
