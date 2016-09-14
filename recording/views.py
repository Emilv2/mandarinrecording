from django.shortcuts import render
from django.template.context_processors import csrf
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.html import escape

@login_required()
def recording(request):
    csrf_token = {}
    csrf_token.update(csrf(request))
    context = {}

    return render(request, 'recording.html', context)

def upload(request):
    customHeader = request.META['HTTP_MYCUSTOMHEADER']
    # obviously handle correct naming of the file and place it somewhere like media/uploads/
    uploadedFile = open("recording.ogg", "wb")
    # the actual file is in request.body
    uploadedFile.write(request.body)
    uploadedFile.close()
    # put additional logic like creating a model instance or something like this here
    return HttpResponse(escape(repr(request)))
