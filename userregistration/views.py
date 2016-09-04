from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .models import ContributorCreationForm, CustomUserCreationForm
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

def registration(request):
    csrf_token = {}
    csrf_token.update(csrf(request))

    user_form = CustomUserCreationForm(request.POST)
    contributor_form = ContributorCreationForm(request.POST)
    if all((user_form.is_valid(), contributor_form.is_valid())):
        user = user_form.save()
        contributor = contributor_form.save(commit=False)
        contributor.user = user
        contributor.save()
        return HttpResponseRedirect('/thanks/')

    context = {'user_form' : user_form,
            'contributor_form' : contributor_form}
#TODO
    return render(request, 'registration.html', context)
