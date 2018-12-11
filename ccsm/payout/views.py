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