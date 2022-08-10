from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import is_valid_path
from .models import Post
from .forms import PostForm

def index(request):
    #If method is POST
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        #If the form is valid
        if form.is_valid():
            #Yes, Save
            form.save()

            #Redirect to Home
            return HttpResponseRedirect('/')

        else:    
            #No, Show Error 
            return HttpResponseRedirect(form.erros.as_json())

   #Get all posts, limit = 20
    posts = Post.objects.all().order_by('-created_at')[:20]
    form = PostForm()


    #Show
    return render(request, 'posts.html',
                    {'posts':posts})


def delete(request, post_id):
    #Find post
    post = Post.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect('/')

def edit(request, post_id):
    # Find post
    post = Post.objects.get(id=post_id)
    if request.method == 'GET':
        return render(request, 'edit.html', {'post': post})

    if request.method == 'POST':
        ep= Post.objects.get(id= post_id)
        form = PostForm(request.POST, request.FILES, instance=ep)

        # If the form is valid
        if form.is_valid():
            # Yes, Save
            form.save()

        # Redirect to Home
        return HttpResponseRedirect('/')


def like(request,post_id):
    post=Post.objects.get(id=post_id)
    new_value=post.likes +1
    post.likes=new_value
    post.save()
    return HttpResponseRedirect('/')