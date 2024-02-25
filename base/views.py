from django.shortcuts import render, redirect
from .models import User, Event, Submission
from .forms import SubmissionForm, CustomCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponse
# from django.contrib.auth.forms import UserCreationForm  

# Create your views here.

def login_page(request):
    page ='login'
    if request.method == 'POST':
        user = authenticate(email=request.POST.get('email'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            return redirect('home')
    context = {'page':page}
    return render(request, 'login_register.html', context)

def register_page(request):
    form = CustomCreationForm()
    if request.method == 'POST':
        form = CustomCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) 
            user.save()
            login(request, user)
            return redirect('home')
        
        
    page ='register'
    context = {'page':page, 'form':form}
    return render(request, 'login_register.html', context)

def logout_user(request):
    logout(request)
    return redirect('login')
    

def home_page(request):
    users = User.objects.filter(hackthon_participant=True)
    events = Event.objects.all()
    context = {'users': users, 'events': events}
    return render(request, 'home.html', context)


def user_page(request, pk):
    user = User.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def account_page(request):
    user = request.user
    context = {'user': user}
    return render(request, 'account.html', context)

def event(request, pk):
    event = Event.objects.get(id=pk)
    registered = False
    submitted = False
    if request.user.is_authenticated:
        registered = request.user.events.filter(id=event.id).exists()
        submitted = Submission.objects.filter(participant=request.user, event=event).exists()
    context = {'event': event, 'registered': registered, 'submitted': submitted}
    return render(request, 'event.html', context)

@login_required(login_url='login')
def registration_confirmation(request, pk):
    event = Event.objects.get(id=pk)
    context = {'event': event}
    if request.method == 'POST':
        event.participants.add(request.user)
        return redirect('event', event.id)
    return render(request, 'event_confirmation.html', context)

@login_required(login_url='login')
def project_submission(request, pk):
    event = Event.objects.get(id=pk)
    form = SubmissionForm( initial={'event': event, 'participant': request.user})
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, initial={'event': event, 'participant': request.user})
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'event': event, 'form': form}
    return render(request, 'submit_form.html', context) 

@login_required(login_url='login')
def update_submission(request,pk):
    submission = Submission.objects.get(id=pk)
    
    if request.user != submission.participant:
        HttpResponse('You are not allowed to be here.')
    event = submission.event
    form = SubmissionForm(instance=submission)
    if request.method == 'POST':
        form = SubmissionForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            return redirect('account')
    
    context = {'form': form, 'event': event}
    return render(request, 'submit_form.html', context)






