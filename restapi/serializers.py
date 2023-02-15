from rest_framework import serializers
from .models import Country, CovidCase
from django.contrib.auth.models import User


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        user = serializers.PrimaryKeyRelatedField(source='user', queryset=User.objects.all())
        model = Country
        fields = ['id','name']
   
        
class CovidCaseSerializer(serializers.ModelSerializer):
    class Meta:
        country = serializers.PrimaryKeyRelatedField(source='country', queryset=Country.objects.all())
        model = CovidCase
        fields = ['id','country','country_code','confirmed','deaths','recovered','date']
