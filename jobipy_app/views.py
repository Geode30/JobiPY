from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import api_views


# Create your views here.

def index(request):
    
    if 'user_id' not in request.session:
        return render(request, 'jobipy/index.html')
    
    if request.session['user_id'] > 0:
        return HttpResponseRedirect(reverse('jobs'))
    else:
        return render(request, 'jobipy/index.html')

def register(request):
    if 'user_id' not in request.session:
        return render(request, 'jobipy/register.html')
    
    if request.session['user_id'] > 0:
        return HttpResponseRedirect(reverse('jobs'))
    else:
        return render(request, 'jobipy/register.html')

def login(request):
    if 'user_id' not in request.session:
        return render(request, 'jobipy/login.html')
    
    if request.session['user_id'] > 0:
        return HttpResponseRedirect(reverse('jobs'))
    else:
        return render(request, 'jobipy/login.html')

def setup(request):
    if 'user_id' not in request.session:
        return render(request, 'jobipy/index.html')
    
    if request.session['user_id'] > 0:
        return render(request, 'jobipy/setup.html')
    else:
        return HttpResponseRedirect(reverse('index'))
    
def jobs(request):
    if 'user_id' not in request.session:
        return render(request, 'jobipy/index.html')
    
    if request.session['user_id'] > 0:
        return render(request, 'jobipy/jobs.html')
    else:
        return HttpResponseRedirect(reverse('index'))

def post(request):
    if 'user_id' not in request.session:
        return render(request, 'jobipy/index.html')
    
    if request.session['user_id'] > 0:
        return render(request, 'jobipy/post.html')
    else:
        return HttpResponseRedirect(reverse('index'))

def profile(request):
    if 'user_id' not in request.session:
        return render(request, 'jobipy/index.html')
    
    if request.session['user_id'] > 0:                
        image_path = api_views.display_resume_img(request.session['user_id'])
        return render(request, 'jobipy/profile.html', {
            'image_path': image_path
        })
    else:
        return HttpResponseRedirect(reverse('index'))
    
def posted(request):
    if 'user_id' not in request.session:
        return render(request, 'jobipy/index.html')
    
    if request.session['user_id'] > 0:
        return render(request, 'jobipy/posted.html')
    else:
        return HttpResponseRedirect(reverse('index'))

def message(request, group_name):
    return render(request, 'jobipy/message.html', {
        'group_name': group_name
    })