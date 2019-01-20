import calendar
import datetime
import json
import time
import firebase_admin
import paypalrestsdk
import requests
import random
import string
import smtplib
from email.mime.text import MIMEText
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials
from firebase_admin import db
from paypalrestsdk import Payout
# Fetch the service account key JSON file contents
# Note follow this flow to keep our files interchangeable
#cred = credentials.Certificate('/Users/caleblee/Desktop/CCServer/ccsm/payout/ServiceAccountKey.json')
#cred = credentials.Certificate('CCServer/ccsm/payout/ServiceAccountKey.json')
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "clickerclash",
  "private_key_id": "5ae4e01d505b9bbc66982e62d6394aa2ffc732d1",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCi+UMweaOf6tUK\nJn6LSbwniGilKx6pUPdoIePkKNHwtGhuPmGHlZARCcBo9qSoq/9btzratw3Fo9oH\niun/6U8CrADlFaWlkpsWfxCLA3f/rm4Ti/pFohdXmwPWmtz1b3ODxE+yj8ptMq53\nlUhRd46YfzV4o1U9unG0QuJ86BZF/1nCc37Fvy76mZxF38YUZJm4oGGcUoHWH3wB\ngYFk0mYSW3rqVhHg4Eony2m9fxSzUnHdgNOWF7EOvA8o3iVr2blJ4pkqq0N/pbTF\n+Wo8SrKIqFAebyTCE9kCSJsKsUk4Fomn7QPqFgkA8NI9dcS3RiCoE34IiSt+QFbo\nway0nsLLAgMBAAECggEADcn7Rlm0X252EgLJyC037zxaZkcss/S2yie76W0Ovkf1\nYgaDJ/6ejuJ9ViQwMFlFJNRu9VxxnNxNMUAupkluNvKorLlVJ5os5w1fL/PeLlLq\n21qHlWauhOoHvBukQFvqsSZl+9ywquaT3mhSExqDhSGWO5vONYfV4QObuCfG4qsi\nqYR/ZimYzVoTiCUFBqcu9lZjB+1YrU4z0FZ6SCauc+aNhQfO3TfTmmXHaGte39n8\nu1jiJW/IUwULPWbefst6n8UNBgWwLJ51+6YDJj0tounkKmNKMOJRj4Lo6IPe+V1u\nF7s3fahTP4+Mic4oALId7p6bhKH47JGMGlvmug+fgQKBgQDWOQgEozqH35rVS9iz\nZE7T7KR+pse/S9SyOqyOrFv6D0WMCtFl0Xm3Ju1OVhga65K6hTjJGo1WWDd9/Y0G\nQKkpghEVpnsxucstFxNf4zxVBdTNAzwWyI5Nnz4nKYtMl2KhPVgJmpVM+lnZ5Xpu\nOmah2uiE/9T80/OhtZNUmNnwiwKBgQDCwaUNVU2Htrl8IOvrIyAV91G902gbMsOC\n4mFoa1Fp6Fq0HvAEVOW6d2iegtYKqtqyhyjPDMmRqWOjM0Cw1+eBRbuX9xzO9DkN\nv8vTlNQD2V3H4h13sNSEVMDXiTWF08qxj8dh9oAACTsLq+3F/VouHMhChZxtJr78\n8upVzUR+wQKBgCL949pmEzx4gOEQZ5A99UZWpDPv6DbOGysVvHP9oXSCJBkQ901L\nXzdUi3S9SWi0TB5dfn4S8T1GYaIZ1XxM+ZTHIyVHMV5Y++AcodSK2KMGtdDbE2ih\nT+VL+qoI9jEHlVvDGmtPLc4KIr0d59azgWo0yMBYzaCSunwSncM2yHqrAoGBALCn\nHwQiDMn95u79maBV4wOpqp5JRNPuzsJIftxNA7LRzHw217TGIP5q0x18RZO1d9uZ\nl11/FtKl17evhI0juVxbmRX1Uk8x3RJolwRaqZi4MEVfByWK4qkJi0W1sjOqcN9w\nMATepynhNYqXr3v4GzVabBdSxBmJnJEp8X5USz3BAoGAVecBUgBgUgE97rc6e6il\n12Tz628P02viZgIFrSBIyX6KK0TyQx1uIWpKWVg458e3ZtuSLHLkdGKPLFa3Xvqr\n8fd6GB1Tn58CDXLY7sWqjbFsfp7wK1mn6kkoRXRGnu/torM0YgjjxAxf17mAXpnh\n+k4JqZscu/I+t772PXmCakE=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-jimla@clickerclash.iam.gserviceaccount.com",
  "client_id": "112212190906725573877",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-jimla%40clickerclash.iam.gserviceaccount.com"
})
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://clickerclash.firebaseio.com/'
})

ref = db.reference()





def getAccessToken():
    url = 'https://api.sandbox.paypal.com/v1/oauth2/token'
    client_id = 'ASsYedLneAfnAb1gDKswsaZh4ia46AN1MIjlbj_JYfuGJco8J3O4S6vzXlqFEoYRBVqVUV0XwQjyIW7n'
    secret = 'EGma-gmh-mW2Ra6ohybDK_YXgNKfIM7aYxcSM_9fdfqDiuwXEdvTO5ShePwGVgpwNdR-cHPvciJNc_op'
    header = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'content-type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
    }
    r = requests.post(url, data=data, headers=header, auth=(client_id, secret)).json()
    print(r['access_token'])
    print(r['expires_in'])
    return r['access_token']


def paypalConfirmed(username, email, uid, exactRequestDate):
    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": "ASsYedLneAfnAb1gDKswsaZh4ia46AN1MIjlbj_JYfuGJco8J3O4S6vzXlqFEoYRBVqVUV0XwQjyIW7n",
        "client_secret": "EGma-gmh-mW2Ra6ohybDK_YXgNKfIM7aYxcSM_9fdfqDiuwXEdvTO5ShePwGVgpwNdR-cHPvciJNc_op"
    })
    '''
    url = 'https://api.paypal.com/v1/payments/payouts?sync_mode=false'
    header = {
        'Accept': 'application/json',
        'Authorization': 'Bearer ' + getAccessToken(),
        'Content-Type': 'application/json'
    }
    '''
    sender_batch_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
    payout = Payout({
        "sender_batch_header": {
            "sender_batch_id": sender_batch_id,
            "email_subject": "Click Clash: You have a payment!",
            "email_message": "This is a cashout prize for: " + username + ". Your User ID is: " + uid +
                             ". This was sent on " + exactRequestDate + "."
        },
        "items": [
            {
                "recipient_type": "EMAIL",
                "amount": {
                    "value": 5.00,
                    "currency": "USD"
                },
                "receiver": email,
                "note": "Thank you and enjoy your prize! Email clickerclash.business@gmail.com for disputes.",
                "sender_item_id": "Standard Cashout"
            }
        ]
    })
    if payout.create(sync_mode=False):
        print("payout[%s] created successfully" %
              (payout.batch_header.payout_batch_id))
        paymentHistory = open("payouthistory.txt", "a")
        paymentHistory.write("Username: " + username + "\n")
        paymentHistory.write("UID: " + uid + "\n")
        paymentHistory.write("Email: " + email + "\n")
        paymentHistory.write("Date: " + exactRequestDate + "\n")
        paymentHistory.write("Batch ID: " + sender_batch_id + "\n")
        paymentHistory.write("Other: " + payout.batch_header.payout_batch_id + "\n")
        paymentHistory.write("--------------------------------------------" + "\n")
        paymentHistory.close()
        return True
    else:
        print(payout.error)
        return False
def findSMTP(usersProvider):
    #find and match list of user providers
    usersProviderl = usersProvider.lower()
    existingProviders = {'1and1.com': 'smtp.1and1.com', 'airmail.net': 'mail.airmail.net', 'aol.com': 'smtp.aol.com',
                         'att.net': 'outbound.att.net', 'bluewin.ch': 'smtpauths.bluewin.ch', 'btconnect.com':
                         'mail.btconnect.tom', 'comcast.net': 'smtp.comcast.net', 'earthlink.net':
                         'smtpauth.earthlink.net', 'gmail.com': 'smtp.gmail.com', 'gmx.net': 'mail.gmx.net',
                         'hotpop.com': 'mail.hotpop.com', 'libero.it': 'mail.libero.it', 'lycos.com': 'smtp.lycos.com',
                         'o2.com': 'smtp.o2.com', 'orange.net': 'smtp.orange.net', 'outlook.com': 'smtp.live.com',
                         'tin.it': 'mail.tin.it', 'tiscali.co.uk': 'smtp.tiscali.co.uk', 'verizon.net':
                         'outgoing.verizon.net', 'virgin.net': 'smtp.virgin.net', 'wanadoo.fr': 'smtp.wanadoo.fr',
                         'yahoo.com': 'smtp.mail.yahoo.com'}

    return existingProviders.get(usersProviderl)

def getCode(exactRequestDate):
    #payoutcode = open('payoutcodes.txt')
    #payoutcodedata = payoutcode.readlines()
    #currentcode = payoutcodedata[2]
    #print(currentcode)
    #payoutcode.close()
    #payoutcodedata.pop(2)

    #payoutcoderewrite = open('payoutcodes.txt', 'w')
    #newPayoutData = "".join(payoutcodedata)
    #payoutcoderewrite.write(newPayoutData)
    #payoutcoderewrite.close()

    #payoutcodelog = open('oldpayoutcodes.txt', 'a')
    #payoutcodelog.write(currentcode + "Date: " + exactRequestDate + "\n")
    #payoutcodelog.write("--------------------------------------------" + "\n")
    #payoutcodelog.close()
    code1 = ref.child('server').child('codes').child('code1').get()
    if code1 != "":
        ref.child('server').child('expiredcodes').child(code1).set(exactRequestDate)
        ref.child('server').child('codes').child('code1').set("")
        currentCode = code1
        return currentCode
    code2 = ref.child('server').child('codes').child('code2').get()
    if code2 != "":
        ref.child('server').child('expiredcodes').child(code2).set(exactRequestDate)
        ref.child('server').child('codes').child('code2').set("")
        currentCode = code2
        return currentCode
    code3 = ref.child('server').child('codes').child('code3').get()
    if code3 != "":
        ref.child('server').child('expiredcodes').child(code3).set(exactRequestDate)
        ref.child('server').child('codes').child('code3').set("")
        currentCode = code3
        return currentCode
    code4 = ref.child('server').child('codes').child('code4').get()
    if code4 != "":
        ref.child('server').child('expiredcodes').child(code4).set(exactRequestDate)
        ref.child('server').child('codes').child('code4').set("")
        currentCode = code4
        return currentCode
    code5 = ref.child('server').child('codes').child('code5').get()
    if code5 != "":
        ref.child('server').child('expiredcodes').child(code5).set(exactRequestDate)
        ref.child('server').child('codes').child('code5').set("")
        currentCode = code5
        return currentCode


def emailBot(username, email, uid, exactRequestDate):
    print('Starting Email')
    sender = 'clickerclash.business@gmail.com'
    receiver = email
    usersProvider = receiver[receiver.find('@')+1:]
    if findSMTP(usersProvider):
        smtp_server_name = findSMTP(usersProvider)
        port = '465'
        if port == '465':
            server = smtplib.SMTP_SSL('{}:{}'.format(smtp_server_name, port))
        else:
            server = smtplib.SMTP('{}:{}'.format(smtp_server_name, port))
            server.starttls()
        payOutId = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(10))

        currentCode = getCode(exactRequestDate)
        content = f"""Congratulations! Your $10 Amazon gift card code is: {currentCode}
                    
We would greatly appreciate it if you share about your reward on social media and with friends! 
Thank You for playing!
        
        
Important Info For {username}:
User ID: {uid}
Request Date: {exactRequestDate}
Payout ID: {payOutId}
                      
~This No Reply Email was generated by clashBot~
For any issues or inquires please Email clickerclash.business@gmail.com
Best regards,
    WithoutAnyLimit"""

        msg = MIMEText(content)
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = 'Clicker Clash Cashout'
        server.login(sender, password='clobwdtipjbgguob')
        print('Logging Transaction...')
        ref.child('server').child('payoutHistory').child(uid).child('email').set(email)
        ref.child('server').child('payoutHistory').child(uid).child('payoutID').set(payOutId)
        ref.child('server').child('payoutHistory').child(uid).child('requestdate').set(exactRequestDate)
        ref.child('server').child('payoutHistory').child(uid).child('username').set(username)

        #paymentHistory = open("payouthistory.txt", "a")
        #paymentHistory.write("Username: " + username + "\n")
        #paymentHistory.write("UID: " + uid + "\n")
        #paymentHistory.write("Email: " + email + "\n")
        #paymentHistory.write("Date: " + exactRequestDate + "\n")
        #paymentHistory.write("Code ID: " + currentCode)
        #paymentHistory.write("Payout ID: " + payOutId + "\n")
        #paymentHistory.write("--------------------------------------------" + "\n")
        #paymentHistory.close()
        print('Done')
        server.send_message(msg)
        server.quit()
        print('Email Sent')
        return True
    else:
        print('Error')
        return False

    #check for provider
    #check port
    #finish login send and quit





#checking to see if request works/does
def getRequest(request):
    #endTime = ref.child('tournaments').child('standard').child('st1').child('endDate').get()
    #print(endTime)
    responseData = {
        'id': 4,
        'date': "12/11/2018",
        'ccValue': 5
    }
    return JsonResponse(responseData)

#Added exempt this isnt safe lol
@csrf_exempt
def postRequest(request):
    if request.method == 'POST':
        #createfile = open("payouthistory.txt", "w")
        #createfile.write("Payout History Log")
        #createfile.close()
        body = json.loads(request.body)
        print(json.dumps(body))
        username = body['username']
        email = body['email']
        uid = body['uid']
        ccValue = body['ccValue']
        timestamp = body['date']
        clientKey = body['clientKey']
        print(username)
        print(email)
        print(uid)
        print(ccValue)
        print(timestamp)
        print(clientKey)
        requestDate = datetime.datetime.fromtimestamp(timestamp)
        exactRequestDate = requestDate.strftime('%m-%d-%Y %H:%M:%S')
        print(exactRequestDate)
        if verifyRequest(username, uid, ccValue, timestamp, clientKey):
            print('Passed all checks')
            adjustccValues(username, uid, ccValue)
            print('Adjusted User CC Value')
            if emailBot(username, email, uid, exactRequestDate):
                print('Success! Returning Response To Client')
                return JsonResponse({'status': 'passed', 'message': 'Payout Complete'})
            else:
                print('Failure! Returning Response To Client')
                return JsonResponse({'status': 'failedPayout', 'message': 'Payout Incomplete'})


            #if paypalConfirmed(username, email, uid, exactRequestDate):
                #return JsonResponse({'status': 'passed', 'message': 'hello'})
            #else:
                #return JsonResponse({'status': 'failedPayout', 'message': 'goodbye'})
        else:
            print('Failed checks')
            return JsonResponse({'status': 'failedChecks', 'message': 'goodbye'})
    return HttpResponse("Ok")


def adjustccValues(username, uid, ccValue):
    #Subtracting 1000 CC from user
    adjustedValue = ccValue - 1000
    ref.child('clashCoins').child(username).child(uid).child('cc').set(adjustedValue)



def verifyRequest(username, uid, ccValue, timestamp, clientKey):
    print('Verify Request')
    payoutLockStatus = ref.child('payout').child('status').get()
    if payoutLockStatus == 'unlocked':
        print('Lock         [Passed]')
        winCheck = ref.child('users').child(uid).child('tWins').get()
        if winCheck != 0:
            print('WinCheck     [Passed]')
            #Username and Uid Check
            unCheck = ref.child('users').child(uid).child('username').get()
            uidConfirm = ref.child('usernames').child(username).get()
            checkCCvalue = ref.child('clashCoins').child(username).child(uid).child('cc').get()
            if username == unCheck and uid == uidConfirm and checkCCvalue == ccValue and checkCCvalue >= 1000:
                print('UN|UID|CC    [Passed]')
                #Last check for request time
                clientTS = timestamp
                serverTS = calendar.timegm(time.gmtime())
                #5 mins
                threshHoldS = serverTS - clientTS
                if threshHoldS <= 300:
                    print('TimeCheck    [Passed]')
                    if clientKey == "yea_im_feeling_like_ray_charles":
                        print('ClientCheck  [Passed]')
                        return True
                    #Request is recent enough
                    else:
                        print('ClientCheck  [Failed]')
                        return False
                else:
                    print('TimeCheck    [Failed]')
                    return False
                    #Old request return error
            else:
                print('UN|UID|CC    [Failed]')
                return False
                #return error message to client

        elif winCheck == 0:
            print('WinCheck     [Failed]')
            #return error message to client
            return False
    elif payoutLockStatus == 'locked':
        print('Lock         [Failed]')
        return False
        #return error message to client



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