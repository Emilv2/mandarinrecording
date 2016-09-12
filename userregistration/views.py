from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import ContributorCreationForm, CustomUserCreationForm, \
        AudioCaptchaForm
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login

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
        contributor = authenticate(
                username=user_form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                )
        login(request, contributor)
        return HttpResponseRedirect('/recording/')

    audio_files = ['audio_file.mp3', 'audio_file.mp3', 'audio_file.mp3']
    context = {'user_form' : user_form,
            'contributor_form' : contributor_form,
            'captcha_list' : captcha_list,
            'audio_files' : audio_files}
    #TODO
    return render(request, 'registration.html', context)

def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/recording/')
        else:
            pass
            #TODO hReturn a 'disabled account' error message
    else:
        #TODO show some login error message
        return HttpResponseRedirect('/login/')

#TODO
def password_reset(request):
    pass
