# Create your views here.

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login


from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from lyspizza.main.models import *

import datetime

@login_required
def index(request):
    occasions = list(Occasion.objects.all())
    occasions.sort(reverse=True)
    return render_to_response('index.html', {'title': 'Home',
                                             'coming': [x for x in occasions if x.date >= datetime.date.today()],
                                             'past': [x for x in occasions if x.date < datetime.date.today()]},
                              RequestContext(request))

@login_required
def occasion_view(request, occasion_id):
    ocsn = get_object_or_404(Occasion, pk=occasion_id) 
    attn = Attendance.objects.filter(occasion = ocsn)

    return render_to_response('occasion.html', {'title': 'Occasion: ' + str(ocsn), 'ocsn': ocsn, 'attn': attn})


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return HttpResponseRedirect('/')
            
    return render_to_response('register.html', {'title': 'Register',
                                                'form': form})
