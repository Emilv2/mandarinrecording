from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import ContributorCreationForm, CustomUserCreationForm, \
        AudioCaptchaForm
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

def registration(request):
    csrf_token = {}
    csrf_token.update(csrf(request))

    user_form = CustomUserCreationForm(request.POST)
    contributor_form = ContributorCreationForm(request.POST)

    captcha_list = [AudioCaptchaForm(request.POST) for i in range(3)]

    if all((user_form.is_valid(), contributor_form.is_valid())) and \
            all( i.is_valid() for i in captcha_list):
        user = user_form.save()
        contributor = contributor_form.save(commit=False)
        contributor.user = user
        contributor.save()
        return HttpResponseRedirect('/thanks/')

    audio_files = ['audio_file.mp3', 'audio_file.mp3', 'audio_file.mp3']
    context = {'user_form' : user_form,
            'contributor_form' : contributor_form,
            'captcha_list' : captcha_list,
            'audio_files' : audio_files}
    #TODO
    return render(request, 'registration.html', context)
