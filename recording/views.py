from django.shortcuts import render
from django.template.context_processors import csrf
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.html import escape
from userregistration.models import get_random_syllables, pretty_pinyin

@login_required()
def recording(request):
    csrf_token = {}
    csrf_token.update(csrf(request))
    context = {}

    return render(request, 'recording.html', context)

def upload(request):
    params = request.body
    pinyin = request.META['HTTP_PINYIN']
#     import pdb; pdb.set_trace()
    # obviously handle correct naming of the file and place it somewhere like media/uploads/
    write_audio_file(
            "{}__{}_{}_{}".format(pinyin,
                request.user.last_name,
                request.user.first_name,
                request.user.username),
            params)
    request.user.contributor.pop_base_syllables_list(pinyin)
    # put additional logic like creating a model instance or something like this here
#     return HttpResponse('teeeeestjeeeees')
    return get_next_syllable(request)

def write_audio_file(filename, data):
    i = 1
    while True:
        try:
            with open("{}_{}.wav".format(filename,str(i).zfill(3)), "xb") as audio_file:
                audio_file.write(data)
            break
        except FileExistsError:
            i += 1

def get_next_syllable(request):
    syllable_list = request.user.contributor.get_base_syllables_list()
    #import pdb; pdb.set_trace()
    if len(syllable_list) > 0:
        next_syllable = syllable_list[0]
    else:
        next_syllable = get_random_syllables()
    return HttpResponse(pretty_pinyin(next_syllable),  content_type="text/plain")

def introduction(request):
    return render(request, 'introduction.html')
