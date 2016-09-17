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
    syllable = "rast"
    # obviously handle correct naming of the file and place it somewhere like media/uploads/
    write_audio_file(
            "{}__{}_{}".format(syllable,
                request.user.last_name,
                request.user.first_name),
            request.body)
    # put additional logic like creating a model instance or something like this here
    return HttpResponse(escape(repr(request)))

def write_audio_file(filename, data):
    i = 1
    while True:
        try:
            with open("{}_{}.wav".format(filename,str(i).zfill(3)), "xb") as audio_file:
                audio_file.write(data)
            break
        except FileExistsError:
            i += 1
