from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, get_user, logout
from django.contrib.auth.models import User
from .forms import EntryForm
from .models import Entry
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect

# Handles user authentication and login
def auth_login(request):
    if request.method == 'POST':  # Check if form is submitted
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if username and password:  # Ensure username and password are provided
            user = authenticate(request, username=username, password=password)
            
            if user is not None:  # If user is authenticated successfully
                login(request, user)
                return redirect('feeling')  # Redirect to 'feeling' page on successful login
            else:
                return HttpResponse("Username or password is incorrect!!")
        else:
            return HttpResponse("Email and password are required!")
    
    return render(request, 'login.html')  # Render login page for GET request

# Handles user registration
def signup(request):
    if request.method == "POST":  # Check if form is submitted
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if email or username already exists
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists!")
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists!")
        
        # Create a new user if both email and username are unique
        user = User.objects.create_user(username=username, email=email, password=password)
        print(f"The user details for registration are: email={email}, username={username}, and password={password}")
        
        return redirect('login')  # Redirect to login page after successful signup
    
    return render(request, 'signup.html')  # Render signup page for GET request

# Ensures user is logged in before accessing the 'feeling' page
@login_required
def feeling(request):
    return render(request, 'feeling.html')

# Ensures user is logged in before accessing the 'home' page
@login_required
def home(request):
    return render(request, 'home.html')

# Displays the journal page with the current user's information
@login_required
def journal(request):
    return render(request, 'journal.html', {"user": request.user})

# Renders the calendar page
@login_required
def calendar(request):
     return render(request, 'calendar.html')

# Renders the tags page
@login_required
def tags(request):
     return render(request, 'tags.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

# Handles the creation of a new journal entry
@login_required
def create_entry(request):
    if request.method == 'POST':  # Check if form is submitted
        journal_form = EntryForm(request.POST, request.FILES)
        print(journal_form.errors)  # Print form errors if any
        if journal_form.is_valid():  # Validate the form
            entry = journal_form.save(commit=False)  # Save form but don't commit to database yet
            entry.user = request.user  # Assign current user to the entry
            entry.save()  # Save entry to the database
            return redirect('entries')  # Redirect to entries list after saving
    else:
        journal_form = EntryForm()  # Create an empty form for GET request
    return render(request, 'journal.html', {'form': journal_form})

# Displays a list of all journal entries
@login_required
def entries(request):
    entries = Entry.objects.all()  # Fetch all entries from the database
    return render(request, 'entries.html', {'entries': entries})

# Handles editing of a journal entry
@login_required
def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)  # Fetch the specific entry by ID

    if request.method == 'POST':  # Check if form is submitted
        title = request.POST.get('title')
        content = request.POST.get('content')
        entry_image = request.POST.get('entry_image')

        # Update entry fields with new data
        entry.title = title
        entry.content = content
        entry.entry_image = entry_image
        entry.save()  # Save the updated entry to the database
        return redirect('entries')  # Redirect to entries list after updating
    else:
        context = {
            'title': entry.title,
            'content': entry.content,
            'entry_image': entry.entry_image
        }
    return render(request, 'journal.html', {'entry': entry, 'context': context})  # Render the form for editing

# Handles the deletion of a journal entry
@login_required
def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)  # Fetch the specific entry by ID
    print(entry.user)  # Print the user who owns the entry
    if request.user == entry.user:  # Check if the logged-in user is the owner of the entry
        entry.delete()  # Delete the entry
        return redirect('entries')  # Redirect to entries list after deletion
    else:
        return redirect('unauthorized_access_error')  # Redirect if unauthorized

# Logs out the current user
@login_required
def dologout(request):
    logout(request)  # Logout the user
    return redirect('login')  # Redirect to login page after logging out
