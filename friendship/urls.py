from django.urls import path
from . import views


urlpatterns = [
    path('add-friend/<int:id>' , views.add_friend , name='add-friend'),
    path('accept-friend-request/<int:id>' , views.accept_friend_request , name='accept-friend'),
    path('reject-friend-request/<int:id>' , views.reject_friend_request , name='reject-friend'),
    path('remove-friend/<int:id>' , views.remove_friend , name='remove-friend'),
    path('friend-post' , views.friend_post , name='friend-post'),
    path('incoming-requests' , views.incoming_requests , name='incoming-requests'),
]
