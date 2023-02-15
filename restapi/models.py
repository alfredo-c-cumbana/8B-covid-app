from django.db import models
from django.contrib.auth.models import User



class Country(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True)
    name = models.CharField(max_length=60)
    
    def __str__(self):
       return self.name
   
class CovidCase(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="country", null=True)
    country_code = models.CharField(max_length=3)
    confirmed = models.CharField(max_length=5)
    deaths = models.CharField(max_length=5)
    recovered = models.CharField(max_length=5)
    date = models.CharField(max_length=30)

    def __str__(self):
        return self.country.name +' '+ str(self.date)
    