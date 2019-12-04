from django.db import models

class Book(models.Model):
    title=models.CharField(max_length=100,unique=True)
    author=models.CharField(max_length=100,unique=True)
    pdf=models.FileField(upload_to='books',unique=True)
    cover=models.ImageField(upload_to="book_cover",unique=True,blank=True,null=True)


    def __str__(self):
        return self.title
