from django.shortcuts import render,redirect
from mgame.models import *
from django.contrib import messages
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.db.models import Q


# Create your views here.

def index(request):
    return render(request,"index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass1']
        password2 = request.POST['pass2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                
                                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model)
                new_profile.save()
                return redirect('dashboard.html')
    else:
        return render(request,'signup.html')

        

 
@login_required(login_url='signin')
def dashboard(request):
    user_object = User.objects.get(username=request.user.username)
    game=event.objects.filter(is_match=False).exclude(user=request.user)
    context = {
    'user_object': user_object,
    'gamedata': game,
    }
    return render(request,"dashboard.html",context)

@login_required(login_url='signin')
def profile(request, pk):
    user_object = User.objects.get(id=pk)
    user_profile = Profile.objects.get(user=user_object)
    ematch=match.objects.all()
    upcoming_matches=[]
    completed_matches=[]
    for i in ematch:
        if i.user1==user_object or i.user2==user_object:
            if not i.game.is_completed:
                upcoming_matches.append(i.game)
            else:
                completed_matches.append(i.game)
                
            
    
    

            
    
    context = {
        'upcoming_matches': upcoming_matches,
        'completed_matches': completed_matches,
        'user_object': user_object,
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')
    
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def addevent(request):
    if request.method =="POST":
        gamename=request.POST['gamename']
        characterid=request.POST['ingamename']
        matchtype=request.POST['matchtype']
        amount=request.POST['amount']
        user_object = User.objects.get(username=request.user.username)
        event1=event.objects.create(
            game=gamename,
            user1ingame=characterid,
            match_type=matchtype,
            amount=amount,
            user_id=user_object.id
        )
        match.objects.create(
            game_id=event1.id,
            user1_id=user_object.id
        )
        return redirect("dashboard")
    return render(request,"add event.html")

def event_detail(request, event_id):
    # Retrieve the event object based on the provided event_id
    event_obj = event.objects.get(id=event_id)
    user_object = User.objects.get(username=request.user.username)
    match_object=match.objects.get(game_id=event_id)

    if request.method == 'POST':
        new_room_id = request.POST.get('new_room_id')
        event_obj.room_id = new_room_id
        event_obj.save()

        ingame_name = request.POST.get('ingame_name')
        event_obj.user2ingame = ingame_name
        event_obj.is_match = True
        event_obj.save()
        if ingame_name:
            match_object.user2=user_object
            match_object.save()
        

    # Pass the event object to the template for rendering
    context = {
        'event': event_obj,
        'user_object': user_object,
    }

    return render(request, 'event_detail.html', context)

def update_room_id(request, event_id):
    event_obj = event.objects.get(id=event_id)

    if request.method == 'POST':
        new_room_id = request.POST.get('new_room_id')
        event_obj.room_id = new_room_id
        event_obj.save()
        return redirect('event_detail', event_id=event_id)

    return redirect('event_detail', event_id=event_id)
def complete_event(request, event_id):
    event_obj = event.objects.get(id=event_id)
    event_obj.is_completed = True
    event_obj.save()

    return redirect('/dashboard')



    
        
