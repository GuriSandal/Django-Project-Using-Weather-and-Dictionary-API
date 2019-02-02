from django.db import models

class City(models.Model):
    name = models.CharField(max_length=25, unique=True)
    def __str__(self):
        return self.name.title()

    class Meta:
        verbose_name_plural = 'cities'

class UserData(models.Model):
    Name = models.CharField(max_length = 100)
    Age = models.PositiveIntegerField()
    Email = models.EmailField(max_length = 100)
    Feedback = models.TextField()

    def __str__(self):
        return self.Name
