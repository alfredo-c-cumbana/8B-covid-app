from django.core.management.base import BaseCommand
from rest_framework import status
import requests

from restapi.models import CovidCase
from restapi.models import Country

class Command(BaseCommand):
    """_Management command to use covid19api to get daily totals for confirmed, 
    recovered, and death cases for the countries user subscribed for_

    Args:
        BaseCommand (_str_): _application domain_
        BaseCommand (_str_): _authentication token_

    Returns:
        
    """
    help ='provide url domain and token eg.: python manage.py dailytotals http://127.0.0.1:800 d774431c2bfd75d774431c2bfd75'
    
    def add_arguments(self, parser):
        parser.add_argument('domain', nargs='+', type = str, help = 'application domain')
        parser.add_argument('token', nargs='+', type = str, help = 'authentication token')
    
    def handle(self, *rgs, **kwargs):
        domain = kwargs['domain'][0]
        token = kwargs['token'][0]
        api_url = domain+'/api/countries/'
        headers = {'Authorization': 'Token {}'.format(token)}

        countries = requests.get(url=api_url, headers=headers)
        if countries.status_code==status.HTTP_401_UNAUTHORIZED:
            return 'Invalid Token'
    
        for country in countries.json():

            api_response = requests.get('https://api.covid19api.com/total/dayone/country/'+country['name'])

            if api_response.status_code == status.HTTP_200_OK:
                temp_country = Country(country['id'],country['name'])
                covid_cases = api_response.json()

                for case in covid_cases:
                    covid_case = CovidCase(
                        country = temp_country,
                        country_code = case['CountryCode'],
                        confirmed = case['Confirmed'],
                        deaths = case['Deaths'],
                        recovered = case['Recovered'],
                        date = case['Date']
                    )
                    covid_case.save()
            else:
                return 'an error has occurred'