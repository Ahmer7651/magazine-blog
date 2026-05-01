from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import MagazineForm, LoginForm, SignupForm, SearchForm
from .models import *
from django.db.models import Q
# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        form= SignupForm(request.POST)
        if form.is_valid():
            user=form.save()
            auth_login(request, user)
            messages.success(request,f'Welcome {user.first_name} your account has been created')
            return redirect('home')
        else:
            messages.error(request, 'Enter correct credentials')
    else:
        form=SignupForm()
    
    return render(request, 'home/signup.html',{'form':form})
        

def log_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method=='POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user=authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Welcome back {username}!')
            return redirect(home)
        else:
            messages.error(request, f'Invalid username or password')

    else:
        form= LoginForm()
      
    return render(request, 'home/login.html', {'form':form})

def log_out(request):
    auth_logout(request)
    messages.success(request,'You have been successfully logged out')
    return redirect(log_in)

    

@login_required
def create_magazine(request):
    if request.method=='POST':
        form=MagazineForm(request.POST, request.FILES)
        if form.is_valid():
            magazine=form.save(commit=False)
            magazine.author=request.user
            magazine.save()
            messages.success(request,f'Magazine "{magazine.title}" created successfully')
            return redirect('home')
    else:
        form=MagazineForm()
    return render(request,'home/create.html',{'form':form})


@login_required
def edit_magazine(request, slug):
    """Edit an existing magazine"""
    
    # Get the magazine or return 404 if not found
    magazine = get_object_or_404(Magazine, slug=slug)
    
    # Check if the logged-in user is the author
    if magazine.author != request.user:
        messages.error(request, 'You can only edit your own magazines.')
        return redirect('home')
    
    if request.method == 'POST':
        form = MagazineForm(request.POST,request.FILES, instance=magazine)
        if form.is_valid():
            form.save()
            messages.success(request, f'Magazine "{magazine.title}" has been updated!')
            return redirect('profile',username=request.user.username)
    else:
        form = MagazineForm(instance=magazine)
    
    return render(request, 'home/edit.html', {'form': form, 'magazine': magazine})

@login_required
def delete_magazine(request, slug):
    """Delete a magazine"""
    
    magazine = get_object_or_404(Magazine, slug=slug)
    
    if magazine.author != request.user:
        messages.error(request, 'You can only delete your own magazines.')
        return redirect('home')
    
    magazine_title = magazine.title
    
    magazine.delete()
    
    messages.success(request, f'Magazine "{magazine_title}" has been deleted successfully.')
    
    return redirect('profile', username=request.user.username)

@login_required
def home(request):
    form=SearchForm(request.GET or None)
    search_query=''
    magazine_list=Magazine.objects.all()
    if form.is_valid() and form.cleaned_data.get('query'):
        search_query=form.cleaned_data.get('query')
        magazine_list = magazine_list.filter(
            Q(title__icontains=search_query) |
            Q(category__name__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )

    magazine_list=magazine_list.order_by('-id')
    paginator=Paginator(magazine_list,5)
    page_number=request.GET.get('page',1)
    magazines=paginator.get_page(page_number)
    return render(request, 'home/index.html',{
        'magazines':magazines,
        'form':form,
        'search_query':search_query
        })

@login_required
def profile(request, username):
    user=get_object_or_404(User, username=username)
    user_magazines=Magazine.objects.filter(author=request.user)
    return render(request, 'home/profile.html',{'profile_user':user,'user_magazines':user_magazines})

@login_required
def magazine_detail(request, slug):
    magazine = get_object_or_404(Magazine,slug=slug)
    return render(request, 'home/detail.html',{'magazine':magazine})