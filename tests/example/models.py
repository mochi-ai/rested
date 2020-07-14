from rested import models

class Person(models.Model):
    name = models.TextField()
    avatar = models.FileField()
