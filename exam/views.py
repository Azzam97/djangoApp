from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Team
import bcrypt

# Create your views here.

def index(request):
    return render(request, "logreg.html")


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)
        return redirect('/')
    else:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        request.session['status'] = "You have registered successfully"
        request.session['name'] = name
        User.objects.create(username = name,
                        email = email,
                        password = pw_hash
                        )
        return redirect('/success')


def success(request):
    if 'name' not in request.session:
        return redirect('/')
    context = {
        'name': request.session['name'],
        'status': request.session['status'],
        'teams': Team.objects.all()
    }
    return render(request, "dashboard.html", context)


def login(request):
    errors2 = User.objects.login_validator(request.POST)
    if len(errors2) > 0:
        for value in errors2.values():
            messages.error(request, value)
        return redirect('/')
    else:
        email2 = request.POST['email2']
        user = User.objects.filter(email = email2)
        request.session['name'] = user[0].username
        request.session['status'] = "Logged in"
        return redirect('/success')
    

def new(request):
    if 'name' not in request.session:
        return redirect('/')
    return render(request, "create.html")


def create_team(request):
    errors3 = Team.objects.team_validator(request.POST)
    if len(errors3) > 0:
        for value in errors3.values():
            messages.error(request, value)
        return redirect('/teams/new')
    username = request.session['name']
    user = User.objects.get(username = username)
    Team.objects.create(name = request.POST['name'],
                        skill = request.POST['skill'],
                        day = request.POST['day'],
                        created_by = User.objects.get(id = user.id))
    return redirect('/success')


def show(request, id):
    if 'name' not in request.session:
        return redirect('/')
    uploader = Team.objects.get(id = id).created_by
    name = uploader.username
    context = {
            'team': Team.objects.get(id = id),
        }
    if request.session['name'] == name:    
        return render(request, "info_admin.html", context)
    else:
        return render(request, "info_user.html", context)



def edit(request, id):
    if 'name' not in request.session:
        return redirect('/')
    context = {
        'team': Team.objects.get(id = id)
    }
    return render(request, "edit.html", context)


def update_team(request, id):
    errors4 = Team.objects.team_validator(request.POST)
    team = Team.objects.get(id =id)
    if len(errors4) > 0:
        for value in errors4.values():
            messages.error(request, value)
        return redirect(f'/teams/{team.id}/edit')
    else:
        team.name = request.POST['name']
        team.skill = request.POST['skill']
        team.day = request.POST['day']
        team.save()
        return redirect('/success')


def delete(request, id):
    team = Team.objects.get(id = id)
    Team.delete(team)
    return redirect('/success')

def logout(request):
    request.session.flush()
    return redirect('/')
