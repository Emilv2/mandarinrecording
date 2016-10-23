from django.shortcuts import render
from django.template.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
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
    # media/uploads/
    write_audio_file(
        "{}__{}_{}_{}".format(pinyin,
                              request.user.last_name,
                              request.user.first_name,
                              request.user.username),
        params)
    request.user.contributor.pop_base_syllables_list(pinyin)
    return HttpResponse();


def write_audio_file(name, data):
    i = 1
    while True:
        try:
            filename = "{}_{}.wav".format(name, str(i).zfill(3))
            with open(filename, 'xb') as audio_file:
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
    return JsonResponse({
        'pinyin': next_syllable,
        'pretty_pinyin': pretty_pinyin(next_syllable)
        })


def about(request):
    return render(request, 'about.html')
