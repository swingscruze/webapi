from django.db import models

# Create your models here.





class Luxury_car(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    description = models.CharField(max_length=120)


    def __str__(self):
        return f"{self.name} Luxuries"





