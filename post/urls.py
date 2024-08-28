from django.urls import path
from . import views

urlpatterns = [
    path('create-post/' , views.create_post , name='create-post'),
    path('my-posts/' , views.my_posts , name='my-posts'),
    path('post/<uuid:post_id>/' , views.post_details , name='post-details'),
    path('like/<uuid:post_id>/' , views.like_post , name='like-post'),
    path('update/<uuid:id>/' , views.update_post , name='update-post'),
    path('my-posts/delete/<uuid:id>/' , views.delete , name='delete'),

]
