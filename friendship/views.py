from django.shortcuts import render, get_object_or_404, redirect
from .models import Friendship, User
from django.contrib import messages
from django.db.models import Q
from post.models import Post



'''
def add_friend(request, id):
    user_to_add = get_object_or_404(User, id=id)
    try:
        # Check if the friendship already exists
        friendship, created = Friendship.objects.get_or_create(user_from=request.user, user_to=user_to_add)
        return redirect('profile', username=user_to_add.username)
    except:
        return redirect('profile', username=user_to_add.username)
'''



def add_friend(request, id):
    user_to_add = get_object_or_404(User, id=id)
    try:
        friendship, created = Friendship.objects.get_or_create(
            user_from=request.user, user_to=user_to_add,
            defaults={'status': 'Pending'}
        )
        if not created and friendship.status == 'Pending':
            friendship.delete()
        return redirect('profile', username=user_to_add.username)
    except:
        return redirect('profile', username=user_to_add.username)
    


def accept_friend_request(request, id):
    friend_request = get_object_or_404(Friendship, user_from__id=id, user_to=request.user, status='Pending')
    friend_request.status = 'Accepted'
    friend_request.save()
    messages.success(request,f'You are now friends with {friend_request.user_from.username}')
    return redirect('incoming-requests')



def reject_friend_request(request, id):
    friend_request = get_object_or_404(Friendship, user_from__id=id, user_to=request.user, status='Pending')
    friend_request.delete()  
    messages.success(request,'Friend request cancelled.')
    return redirect('incoming-requests')



def remove_friend(request, id):
    friendship = Friendship.objects.filter(
        (Q(user_from=request.user) & Q(user_to__id=id) & Q(status='Accepted')) |
        (Q(user_from__id=id) & Q(user_to=request.user) & Q(status='Accepted'))
    ).first()

    if friendship:
        friendship.delete()  
    messages.success(request, 'Friendship removed successfully.')
    return redirect('incoming-requests')



def friend_post(request):
    friendships = Friendship.objects.filter(
        (Q(user_from=request.user) & Q(status='Accepted')) |
        (Q(user_to=request.user) & Q(status='Accepted'))
    )
    
    friend_ids = []
    for friendship in friendships:
        if friendship.user_from == request.user:
            friend_ids.append(friendship.user_to.id)
        else:
            friend_ids.append(friendship.user_from.id)
    

    all_posts = Post.objects.filter(user__id__in=friend_ids)

    context = {
        'posts': all_posts
    }
    return render(request, 'friendship/friend_posts.html', context)



def incoming_requests(request):
    all_requests = Friendship.objects.filter(user_to = request.user , status = 'Pending')
    my_friends = Friendship.objects.filter(
        (Q(user_from=request.user) | Q(user_to=request.user)),
        status='Accepted'
    )
    context ={
        'all_requests': all_requests,
        'my_friends': my_friends
    }
    return render(request , 'friendship/incoming-requests.html', context)
