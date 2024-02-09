from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, ProfileForm, skillForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Profile
from .utils import searchProfiles

# login view
def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User is not Exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username or password incorrect")


    return render(request, 'users/login_register.html')

# logout view
def logoutUser(request):
    logout(request)
    messages.info(request, "User logged out!")
    return redirect('login')

# register user
def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Succesfully Registered")

            login(request, user)
            return redirect('edit-account')
        else:
            messages.success(request, "An error has occurred during registration")

    context = {"page":page, "form": form}
    return render(request, 'users/login_register.html', context)

# Create your views here.
def profiles(request):
    profiles, search_query = searchProfiles(request)
    context = {"profiles":profiles, "search_query":search_query}
    return render(request, 'users/profiles.html',context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")
    context = {"profile":profile, "topSkills":topskills, "otherSkills":otherskills}
    return render(request, 'users/user-profile.html', context)



@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    skills = profile.skill_set.all

    context = {"profile":profile, "skills":skills}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {"form":form}
    return render(request, 'users/profile_form.html', context)


@login_required(login_url='login')
def addSkill(request):
    profile = request.user.profile
    form = skillForm()

    if request.method == "POST":
        form = skillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()

            return redirect('account')

    context = {"form":form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profile
    # print(profile)
    skill = profile.skill_set.get(id=pk)
    # print(skill.description)
    form = skillForm(instance=skill)

    if request.method == "POST":
        form = skillForm(request.POST, instance=skill)
        print(form)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {"form":form}
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSKill(request,pk):
    profile = request.user.profile
    # print(profile)
    skill = profile.skill_set.get(id=pk)
    # print(skill.description)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, "skill deleted successfully!")
        return redirect("account")
    
    context = {"object":skill}
    return render(request, 'users/delete_template.html', context)