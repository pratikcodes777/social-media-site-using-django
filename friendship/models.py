from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Friendship(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]
    
    user_from = models.ForeignKey(User, related_name='friendships_created', on_delete=models.CASCADE)
    user_to = models.ForeignKey(User, related_name='friendships_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        unique_together = ('user_from', 'user_to')

    def __str__(self):
        return f'{self.user_from.username} to {self.user_to.username}: {self.status}'