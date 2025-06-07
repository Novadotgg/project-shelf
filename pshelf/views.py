from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile
from .models import CreatorProject
from .utils import generate_case_study
from .models import VisitorActivity

# Homepage (Landing Page)
def home(request):
    return render(request, 'pshelf/home.html')

# User Registration
def register_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        role = request.POST['role']  # 'visitor' or 'creator'
        # Check password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('register')
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        Profile.objects.create(user=user, user_type=role)
        messages.success(request, "Account created successfully.")
        login(request, user)
        return redirect('creator_dashboard' if role == 'creator' else 'visitor_dashboard')
    return render(request, 'pshelf/register.html')

# User Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if hasattr(user, 'profile'):
                role = user.profile.user_type
                if role == 'creator':
                    return redirect('creator_dashboard')
                else:
                    return redirect('visitor_dashboard')
            else:
                messages.error(request, "User profile not found.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'pshelf/login.html')


# Creator Dashboard
def creator_dashboard_view(request):
    case_study = None

    if request.method == 'POST':
        project = CreatorProject.objects.create(
            user=request.user,
            name=request.POST['Name'],
            stats=request.POST['stats'],
            project_name=request.POST['project_name'],
            project_description=request.POST['project_description'],
            project_image=request.POST.get('project_image', ''),
            project_link=request.POST.get('project_link', ''),
            project_date=request.POST['project_date'],
            project_technologies=request.POST['project_technologies'],
            project_outcomes=request.POST.get('project_outcomes', '')
        )

        # Generate case study using GPT2 (or your function)
        case_study = generate_case_study(project)
        project.case_study = case_study
        project.save()

        messages.success(request, "Project and case study created successfully!")

    return render(request, 'pshelf/creator_dashboard.html', {'case_study': case_study})  
 
 
 
 
def visitor_dashboard_view(request):
    creators = Profile.objects.filter(user_type='creator')
    return render(request, 'pshelf/visitor_dashboard.html', {'creators': creators})
 
 
    
def creator_analytics_dashboard(request):
    user_projects = CreatorProject.objects.filter(user=request.user)
    return render(request, 'pshelf/dash.html', {'projects': user_projects})


def creator_list_view(request):
    creators = Profile.objects.filter(user_type='creator')
    return render(request, 'pshelf/creator_list.html', {'creators': creators})


    
def creator_profile_view(request, username):
    user = User.objects.get(username=username)
    projects = CreatorProject.objects.filter(user=user)
    return render(request, 'pshelf/creator_profile.html', {
        'creator': user,
        'projects': projects
    })
   

def creator_profile_view(request, username):
    user = User.objects.get(username=username)
    projects = CreatorProject.objects.filter(user=user)

    # Track views if logged in and not viewing own profile
    if request.user.is_authenticated and request.user != user:
        for project in projects:
            VisitorActivity.objects.create(
                visitor=request.user,
                creator=user,
                project=project,
                clicked=False  # default
            )

    return render(request, 'pshelf/creator_profile.html', {
        'creator': user,
        'projects': projects
    })

def project_redirect_view(request, project_id):
    project = CreatorProject.objects.get(id=project_id)

    # Mark click if logged in and not the creator
    if request.user.is_authenticated and request.user != project.user:
        VisitorActivity.objects.create(
            visitor=request.user,
            creator=project.user,
            project=project,
            clicked=True
        )

    return redirect(project.project_link)

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

def track_click_view(request, project_id):
    project = get_object_or_404(CreatorProject, id=project_id)

    if request.user.is_authenticated:
        activity = VisitorActivity.objects.filter(
            visitor=request.user, project=project
        ).order_by('-timestamp').first()

        if activity:
            activity.clicked = True
            activity.save()

    return HttpResponseRedirect(project.project_link)

    
# Logout
def user_logout(request):
    logout(request)
    return redirect('home')




# Demo Home (After Login)
def demo_home(request):
    return render(request, 'pshelf/login.html', {'user': request.user})