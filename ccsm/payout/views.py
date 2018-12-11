from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db



# Fetch the service account key JSON file contents
# Note follow this flow to keep our files interchangeable
# Ex all you would have to change is  /jackirish/
cred = credentials.Certificate('/Users/caleblee/Desktop/CCServer/ccsm/payout/ServiceAccountKey.json')
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://clickerclash.firebaseio.com/'
})

ref = db.reference()

#checking to see if request works/does
def payoutRequest(request):
    endTime = ref.child('tournaments').child('standard').child('st1').child('endDate').get()
    print(endTime)
    return HttpResponse(endTime)



# Create your views here.
# Works
#endtime = ref.child('tournaments').child('standard').child('st1').child('endDate').get()
#print(endtime)
'''
import requests




url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
client_id = 'AY4ZGZvODya3HW-4gSpb4wN5QsyrmHN2ZMxZa5NmHmy7pam7h3XNvsju07p7gDm4gAS4qZjqqs69kz_t'
secret = 'EKPf-TSFqNWQ-6crkaGY3ptlfMmVCZedOXYz5s5G4MyOW1qqrVHl3bTODNwXVAu9vnVJa6m_EZV50DUN'

header = {
    'Accept' : 'application/json',
    'Accept-Language' : 'en_US',
    'content-type' : 'application/x-www-form-urlencoded'
}

data = {

    'grant_type': 'client_credentials',
}

r = requests.post(url, data=data, headers=header, auth=(client_id, secret)).json()
print(r['access_token'])
print(r['expires_in'])

'''