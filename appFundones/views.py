from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, get_user, logout
from django.contrib.auth.decorators import login_required
from .models import Post
# Create your views here.
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
            login(request, user)
            return redirect("home")
        
    else:
        loginForm = LoginForm()
    return render(request, "register_login/login.html", {'loginForm': loginForm})
 
 

def logout_view(request):
    logout(request)
    return redirect("login")
    
@login_required
def home_view(request):
    user = get_user(request)
    if request.method == 'POST':
        
        text_post = request.POST.get("text-post")
        image_post = request.FILES.get("image-post")
        
        post = Post(author=user, content=text_post, image=image_post)
        post.save()
        
    all_posts = Post.objects.filter(author=user).order_by('-created_at')
    
    print(all_posts)
    context = {"posts": all_posts, "user": user}
    return render(request, "pages/home.html", context)
        
        