from django.shortcuts import render
from django.template.context_processors import csrf
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required()
def recording(request):
    csrf_token = {}
    csrf_token.update(csrf(request))
    context = {}

    return render(request, 'recording.html', context)
