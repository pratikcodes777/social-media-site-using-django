from django.db import models
from datetime import datetime
from core.models import User
from django.conf import settings
import uuid
# Create your models here.


class Post(models.Model):
    id = models.UUIDField(primary_key=True , default=uuid.uuid4)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images')
    title = models.CharField(max_length=100)
    caption = models.TextField()
    created_at = models.DateTimeField(default=datetime.utcnow )

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
    
    @property
    def is_reply(self):
        return self.parent is not None



class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
