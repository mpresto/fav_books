from django.db import models
from login_app.models import User

# Create your models here.


class BookManager(models.Manager):
    def validator(self, postData):
        errors = {}
        if len(postData['title']) == '':
            errors['title'] = "Title cannot be empty."
        if len(postData['desc']) < 5:
            errors['desc'] = "Description must be at least 5 characters."     
        
        return errors


class Book(models.Model):
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="liked_books")
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = BookManager()

