from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, get_user, logout
from django.contrib.auth.decorators import login_required
from .models import Post, CustomUser, FriendRequest
from django.utils import timezone
from datetime import timedelta


def register_view(request):
    if request.method == 'POST':
        registerForm = RegisterForm(request.POST)
       
        if registerForm.is_valid():
            
            registerForm.save()
            return redirect('login')
    
    else:
        registerForm = RegisterForm()
    return render(request, "register_login/register.html", {'registerForm': registerForm})


def login_view(request):
    if request.method == 'POST':
        loginForm = LoginForm(request.POST)
        if loginForm.is_valid():
            user = loginForm.cleaned_data.get('user')
            if user:
                print("usuario: ", user.email)
                login(request, user)
                return redirect("home")
        
    else:
        loginForm = LoginForm()
    return render(request, "register_login/login.html", {'loginForm': loginForm})
 
 

def logout_view(request):
    logout(request)
    return redirect("login")
    
@login_required(login_url="/login")
def home_view(request):
    user = get_user(request)
    if request.method == 'POST':
        
        text_post = request.POST.get("text-post")
        image_post = request.FILES.get("image-post")
        
        post = Post(author=user, content=text_post, image=image_post)
        post.save()
        
    all_posts = Post.objects.filter(author=user).order_by('-created_at')
    
    post_with_time_difference = []
    date_now = timezone.now()
    for post in all_posts:
        time_difference = date_now - post.created_at
        post_with_time_difference.append({'post': post, 
                                     'time_difference': time_difference}) 
        
   
    context = {"posts": post_with_time_difference, 
               "user": user
            }
    
    return render(request, "pages/home.html", context)
        

@login_required(login_url="/login")
def profile_view(request):
    user = get_user(request)
    if request.method == 'POST':
        image_profile = request.FILES.get("image-profile")
        
        if image_profile:
            if user.profile_image:
                user.profile_image.delete(save=False)
            
            user.profile_image = image_profile
            user.save()
        return redirect("profile")
    
    #tentar melhorar para nao repetir em toda view
    friend_request_notifications = FriendRequest.objects.filter(to_user=user)
    print(friend_request_notifications)
    
    all_posts = Post.objects.filter(author=user).order_by("-created_at")
    
    post_with_time_difference = []
    date_now = timezone.now()
    for post in all_posts:
        time_difference = date_now - post.created_at
        post_with_time_difference.append({'post': post, 
                                     'time_difference': time_difference}) 
        
    
    context = {"user": user, "posts": post_with_time_difference, "notifications": friend_request_notifications}


    return render(request, "pages/my_profile.html", context)
    

@login_required(login_url="/login")
def edit_description_view(request):
    user = get_user(request)
    if request.method == 'POST':
        description_bio = request.POST.get("description-bio")
        user.description_bio = description_bio
        user.save()

    return redirect(profile_view)

@login_required(login_url="/login")
def search_profile_view(request):
    query = request.GET.get('query-profile')
    result = None
    if query:
        result = CustomUser.objects.filter(name=query)
    
    context = {'profiles': result}
    return render(request, "pages/search_profile.html", context)

@login_required(login_url="/login")
def show_profile_view(request, profile_id):
    user = get_object_or_404(CustomUser, id=profile_id)
    print("usuario: ", len(user.friends.all()))
    all_posts = Post.objects.filter(author=user).order_by("-created_at")
    
    post_with_time_difference = []
    date_now = timezone.now()
    for post in all_posts:
        time_difference = date_now - post.created_at
        post_with_time_difference.append({'post': post, 
                                     'time_difference': time_difference}) 

    friend_request_sent = FriendRequest.objects.filter(from_user=get_user(request), to_user=user).exists()
    print(friend_request_sent)

    return render(request, 'pages/someone_profile.html', {'user': user, 'posts': post_with_time_difference, 'friend_request': friend_request_sent})


@login_required(login_url="/login")
def send_friend_request_view(request, profile_id):
    to_user = get_object_or_404(CustomUser, id=profile_id)
    from_user = get_user(request)
    
    if not FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        friend_request = FriendRequest(from_user=from_user, to_user=to_user)
        friend_request.save()
        print("solicitacao de {} para {}.".format(from_user.name, to_user.name))

    return redirect('show_profile', profile_id=profile_id)

@login_required(login_url="/login")
def cancel_friend_request_view(request, profile_id):
    to_user = get_object_or_404(CustomUser, id=profile_id)
    from_user = get_user(request)

    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user):
        friend_request = FriendRequest.objects.filter(from_user=from_user, to_user=to_user)
        friend_request.delete()

    return redirect('show_profile', profile_id=profile_id)

@login_required(login_url="/login")
def add_friend_view(request, friend_id):
    from_user = get_object_or_404(CustomUser, id=friend_id)
    to_user = get_user(request)
    if FriendRequest.objects.filter(from_user=from_user):
        CustomUser.add_friend(to_user, from_user)
        FriendRequest.objects.filter(from_user=from_user, to_user=to_user).delete()

    return redirect("home")

@login_required(login_url="/login")
def decline_friend_view(request, friend_id):
    from_user = get_object_or_404(CustomUser, id=friend_id)
    to_user = get_user(request)
    if FriendRequest.objects.filter(from_user=from_user):
        FriendRequest.objects.filter(from_user=from_user, to_user=to_user).delete()

    return redirect("home")

@login_required(login_url="/login")
def remove_friend_view(request, friend_id):
    user = request.user
    friend = get_object_or_404(CustomUser, id=friend_id)
    
    if user.friends.filter(id=friend_id).exists():
        user.friends.remove(friend)
        friend.friends.remove(user)
        print(friend_id)
                
    
    return redirect("home")