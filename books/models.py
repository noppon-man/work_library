from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    is_rent = models.BooleanField(default=False)
    rent_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title