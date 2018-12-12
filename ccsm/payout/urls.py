from django.urls import path
from . import views

app_name = 'payout'


#when having paths it is server IP/payout/ by default no need to add in before request
urlpatterns = [
    path('getrequest/', views.getRequest, name='grequest'),
    path('postrequest/', views.postRequest, name='prequest'),
]