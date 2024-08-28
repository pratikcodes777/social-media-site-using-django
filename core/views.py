from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth
from django.contrib import messages
from .models import User, Profile
from post.models import Post
# Create your views here.

def index(request):
    all_posts = Post.objects.all().order_by('-created_at')
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None

        for post in all_posts:
            post.is_liked = post.likes.filter(user=request.user).exists()
    
    else:
        for post in all_posts:
            post.is_liked = False

    context = {
        'profile': profile,
        'all_posts': all_posts,
    }
    return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repassword = request.POST.get('repassword')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'User already exists.')
            return redirect('login')
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already taken.')
            return redirect('register')
        if password == repassword:
            new_user = User.objects.create_user(username=username,email=email , password=password)
            new_user.save()

            # create profile picture 
            user_model = User.objects.get(username=username)
            profile = Profile.objects.create(user = user_model , id_user = user_model.id)
            profile.save()

            # settings page 
            user = auth.authenticate(username=username , password=password)
            auth.login(request, user)

            messages.success(request, 'Account created successfully.')
            return redirect('login')
        else:
            messages.info(request, 'Password didnt matched.')
            return redirect('register')

    return render(request , 'user/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username , password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request , f'Logged in successfully. Welcome {request.user}.')
            return redirect('index')
        else:
            messages.warning(request, 'Username and password didnt matched.')
            return redirect('login')
    return render(request , 'user/login.html')


def settings(request):
    user_profile = Profile.objects.get(user = request.user)
    if request.method == 'POST':
        image = request.FILES.get('profile')
        bio = request.POST.get('bio')
        location = request.POST.get('location')

        if image:
            user_profile.profile_img = image
        user_profile.bio = bio
        user_profile.location = location

        user_profile.save()
        return redirect('profile', username=request.user.username)
    context ={
        'user_profile': user_profile
    }
    return render(request, 'user/settings.html', context)



# def profile(request):
#     profile = Profile.objects.get(user = request.user)
#     context ={
#         'profile': profile
#     }
#     return render(request, 'user/profile.html', context)


def profile(request , username):
    user = get_object_or_404(User, username=username)  
    profile = get_object_or_404(Profile, user=user)
    current_user = request.user
    context ={
        'profile': profile,
        'user': user,
        'current_user': current_user
    }
    return render(request, 'user/profile.html', context)




def logout(request):
    auth.logout(request)
    messages.success(request , 'Logged out successfully.')
    return redirect('index')
