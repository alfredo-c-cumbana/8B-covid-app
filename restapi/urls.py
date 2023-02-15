"""restapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from rest_framework import permissions
from django.contrib import admin
from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from restapi import views

schema_view = get_schema_view(
   openapi.Info(
      title="COVID REST API",
      default_version='v1',
      description="Rest api documentaion",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
   authentication_classes = [],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/countries/', views.country_list),
    path('api/countries/<int:id>', views.country_operations),
    path('api/login/', views.login),
    path('api/percentage/<str:country_name>', views.percentage_cases),
    path('api/topthree/<str:case_type>', views.top_three_countries),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
 