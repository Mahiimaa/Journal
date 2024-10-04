from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login, get_user,logout
from django.contrib.auth.models import User
from .forms import EntryForm
from .models import Entry
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

def auth_login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if username and password: 
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('feeling') 
            else:
                return HttpResponse("Username or password is incorrect!!")
        else:
            return HttpResponse("Email and password are required!")
    
    return render(request, 'login.html')

def signup(request):
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists!")
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists!")
        
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"The user details for registration are: email={email}, username={username}, and password={password}")
        
        return redirect('login')
    
    return render(request, 'signup.html')

@login_required
def feeling(request):
    return render(request, 'feeling.html')

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def journal(request):
    return render(request, 'journal.html',{"user":request.user})

@login_required
def calendar(request):
     return render(request, 'calendar.html')

@login_required
def tags(request):
     return render(request, 'tags.html')

@login_required
def create_entry(request):
    if request.method == 'POST':
        journal_form = EntryForm(request.POST, request.FILES)
        print(journal_form.errors)
        if journal_form.is_valid():
            entry = journal_form.save(commit=False)
            entry.user = request.user 
            entry.save()
            return redirect('entries')
    else:
        journal_form = EntryForm()
    return render(request, 'journal.html', {'form': journal_form})

@login_required
def entries(request):
    entries = Entry.objects.all()
    return render(request, 'entries.html', {'entries': entries})

@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        entry_image = request.POST.get('entry_image')

        entry.title = title
        entry.content = content
        entry.entry_image = entry_image
        entry.save()
        return redirect('entries') 
    else:
        context = {
            'title': entry.title,
            'content': entry.content,
            'entry_image': entry.entry_image
        }
    return render(request, 'journal.html', {'entry': entry, 'context': context})


@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    print(entry.user)
    if request.user == entry.user:
        entry.delete()
        return redirect('entries')  
    else:
        return redirect('unauthorized_access_error')

def dologout(request):
    logout(request)
    return redirect('login')