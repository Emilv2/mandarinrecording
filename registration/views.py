from django.shortcuts import render
from .models import ContributorCreationForm, CustomUserCreationForm, \
    AudioCaptchaForm
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import views as auth_views


def registration(request):
    user_form = CustomUserCreationForm(request.POST)
    contributor_form = ContributorCreationForm(request.POST)
    captcha_form = AudioCaptchaForm(request.POST)
    csrf_token = {}
    csrf_token.update(csrf(request))
    context = {'user_form': user_form,
               'contributor_form': contributor_form,
               'captcha_form': captcha_form,
               }

    if request.method == 'POST':
        if all((user_form.is_valid(), contributor_form.is_valid() and \
                captcha_form.is_valid())):
            user = user_form.save()
            contributor = contributor_form.save(commit=False)
            contributor.user = user
            contributor.save()
            contributor = authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password1'],
            )
            login(request, contributor)
            return HttpResponseRedirect('/recording/')
        else:
            return render(request, 'registration.html', context)
    else:
        user_form = CustomUserCreationForm()
        contributor_form = ContributorCreationForm()
        captcha_form = AudioCaptchaForm()

        context = {'user_form': user_form,
                   'contributor_form': contributor_form,
                   'captcha_form': captcha_form,
                   }
        # TODO
        return render(request, 'registration.html', context)


def login(request, *args, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/recording/')
    return auth_views.login(request, *args, **kwargs)


# TODO
def password_reset(request):
    pass
