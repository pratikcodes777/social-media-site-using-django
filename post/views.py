from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import Post, Comment, Like
from core.models import Profile
from django.contrib import messages
# Create your views here.


def create_post(request):
    if request.method == 'POST':
        user = request.user
        image = request.FILES.get('image')
        title = request.POST.get('title')
        caption = request.POST.get('caption')
        new_post = Post.objects.create(user=user , image=image , title=title , caption = caption)
        new_post.save()
        messages.success(request, 'Post created successfully.')
        return redirect('index')
    return render(request, 'post/create_post.html')


'''

def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  
    
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST':
        content = request.POST.get('comment')

        if content:
            Comment.objects.create(
                post=post,
                user=request.user, 
                content=content,
            )
            return redirect('post-details', post_id=post.id)

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked
    }

    return render(request, 'post/post-details.html', context)

'''


def post_details(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.filter(parent=None)  
    
    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(post=post, user=request.user).exists()

    if request.method == 'POST':
        content = request.POST.get('comment')
        parent_id = request.POST.get('parent_id')
        parent_comment = None
        if parent_id:  
            parent_comment = Comment.objects.get(id=parent_id)

        if content:
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                parent=parent_comment  # If parent_comment is None, it's a top-level comment on the post
            )
            return redirect('post-details', post_id=post.id)

    context = {
        'post': post,
        'comments': comments,
        'is_liked': is_liked
    }

    return render(request, 'post/post-details.html', context)



def my_posts(request):
    my_posts = Post.objects.filter(user = request.user)
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None
    context = {
        'my_posts': my_posts,
        'profile':profile
    }
    return render(request, 'post/my-posts.html', context)



def update_post(request , id):
    post_to_update = get_object_or_404(Post , id=id)
    if request.method == 'POST':
        title = request.POST.get('title')
        caption = request.POST.get('caption')
        image = request.FILES.get('image')
        post_to_update.title = title
        post_to_update.caption = caption
        post_to_update.image = image
        post_to_update.save()
        messages.success(request, 'Post updated successfully.')
        return redirect('my-posts')
    context = {
        'post':post_to_update
    }
    return render(request , 'post/update-post.html' , context)

    

def delete(request , id):
    post_to_delete = get_object_or_404(Post , id=id)
    post_to_delete.delete()
    return redirect('my-posts')



def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    liked = Like.objects.filter(user=user, post=post).exists()

    if liked:
        Like.objects.filter(user=user, post=post).delete()
        liked = False
    else:
        Like.objects.create(user=user, post=post)
        liked = True

    return JsonResponse({
        'liked': liked,
        'total_likes': post.total_likes(),
    })


def search(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')
        posts = Post.objects.filter(title__icontains=search_query)
        context = {
            'search_query': search_query,
            'posts': posts,  
        }
        return render(request, 'post/search-results.html', context)

    return render(request, 'post/search-results.html')

