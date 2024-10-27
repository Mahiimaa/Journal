from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
        
class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    entry_image = models.ImageField(upload_to="media/entry-image")
    def __str__(self):
        return self.title

