from .models import Country
from .models import CovidCase
from .serializers import CountrySerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(method='post', operation_description="API for user authentication. It accepts json object with username and password and returns a token.", request_body=openapi.Schema(type=openapi.TYPE_OBJECT, 
    properties={'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),}))
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))  
def login(request):

    username = request.data.get("username")
    password = request.data.get("password") 
 
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', operation_description="API to get the list of added countries.")
@swagger_auto_schema(method='post',operation_description="API to allow users to add a country to monitor COVID-19 cases for.", request_body=openapi.Schema(type=openapi.TYPE_OBJECT, 
    properties={'name': openapi.Schema(type=openapi.TYPE_STRING, description='country name to save/subscribe.'),}))
@csrf_exempt
@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def country_list(request):

    if request.method == 'GET':
        
        account = request.user
        countries = Country.objects.all().filter(user=account)
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)
    
    if request.method == 'POST':
        serializer = CountrySerializer(data = request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='get', operation_description="API to get a specific country by id (primary key).") 
@swagger_auto_schema(method='delete', operation_description="API to delete a country by id (primary key).")        
@swagger_auto_schema(method='put', operation_description="API to update country by id (primary key).", request_body=openapi.Schema(type=openapi.TYPE_OBJECT, 
    properties={'name': openapi.Schema(type=openapi.TYPE_STRING, description='country name to update to'),}))        
@csrf_exempt
@api_view(['GET','PUT', 'DELETE'])
@permission_classes((IsAuthenticated,))
def country_operations(request, id):
    account = request.user
    
    try:
        country = Country.objects.filter(user=account).get(pk=id)
    except Country.DoesNotExist:
        return Response(status = status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer =  CountrySerializer(country)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = CountrySerializer(country, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        country.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)
   
@swagger_auto_schema(method='get', operation_description="API to get a percentage of death cases to confirmed cases for a given country")  
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def percentage_cases(request,country_name):
    account = request.user
    country = Country.objects.all().filter(user=account).filter(name = country_name).get()

    covid_case = CovidCase.objects.all().filter(country = country).latest('date')
    total_deaths = int(covid_case.deaths)
    total_confirmed = int(covid_case.confirmed)
    percentage = round(total_deaths/total_confirmed*100,2)
    return Response({'Percentage': str(percentage)})

@swagger_auto_schema(method='get', operation_description="API to get the top 3 countries (among the subscribed countries) by the total number of cases based on the case type passed by the user (confirmed, death).")  
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def top_three_countries(request,case_type):

    countries = Country.objects.all().filter(user=request.user)
    daily_cases = CovidCase.objects.all()
    cases_by_country = []
    output = {}
    for country in countries:
        covid_case = daily_cases.filter(country = country).latest('date')
        cases_by_country.append(covid_case)
        
    if case_type.lower() == 'confirmed':
        cases_by_country.sort(key=lambda x:int(x.confirmed))
    elif case_type.lower() == 'recovered':
        cases_by_country.sort(key=lambda x:int(x.recovered))
    elif case_type.lower() == 'death':
        cases_by_country.sort(key=lambda x:int(x.deaths))
    else:
        return Response(output)
            
    if len(cases_by_country) > 2:
        for i in range(3):
            output['country '+str(i+1)] = cases_by_country.pop().country.name
    else:
        for i in range(len(cases_by_country)):
            output['country '+str(i+1)] = cases_by_country.pop().country.name
            
    return Response(output)
