from django.shortcuts import render, redirect
from .models import Plan
from .forms import PlanForm
from django.shortcuts import render


def clientPage(request):
    plans = Plan.objects.all()  # Retrieve all plans from the database
    return render(request, 'clientPage.html', {'plans': plans})  # Pass plans to template



def add_plan(request):
    if request.method == "POST":
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientPage')  # Redirect to the subscription page
    else:
        form = PlanForm()

    return render(request, 'add_plan.html', {'form': form})

import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import base64
from datetime import datetime
from .models import MpesaTransaction
from django.contrib.auth.decorators import login_required

@csrf_exempt
def process_mpesa_payment(request):
    print("Received request to process M-Pesa payment.")  # Debugging Print 1

    if request.method == "POST":
        data = json.loads(request.body)
        phone_number = data.get("phone_number")
        try:
            amount = int(float(data.get("amount")))  # Convert to integer
        except (ValueError, TypeError):
            print("Invalid amount format.")  # Debugging Print
            return JsonResponse({"status": "error", "message": "Invalid amount format"})
        
        plan_name = data.get("plan_name")

        print(f"Received Data - Phone: {phone_number}, Amount: {amount}, Plan: {plan_name}")  # Debugging Print 2
        
        # Validate amount
        if amount < 1:
            print("Invalid amount: Must be at least 1 KES.")  # Debugging Print
            return JsonResponse({"status": "error", "message": "Amount must be at least 1 KES"})

        # Validate phone number format
        if not phone_number.startswith("254") or len(phone_number) != 12:
            print("Invalid phone number format.")  # Debugging Print 3
            return JsonResponse({"status": "error", "message": "Invalid phone number format"})

        # Check if user is authenticated, otherwise set to None
        user = request.user if request.user.is_authenticated else None

        # Save transaction as "Pending"
        transaction = MpesaTransaction.objects.create(
            user=user,
            plan_name=plan_name,
            phone_number=phone_number,
            amount=amount,
            status="Pending"
        )
        print("Transaction saved as Pending.")  # Debugging Print 4

        # Get Access Token
        print("Requesting M-Pesa Access Token...")  # Debugging Print 5
        access_token = get_mpesa_access_token()
        
        if not access_token:
            print("Failed to obtain M-Pesa access token.")  # Debugging Print 6
            return JsonResponse({"status": "error", "message": "Failed to obtain M-Pesa access token"})

        print(f"Access Token Received: {access_token}")  # Debugging Print 7

        # STK Push API URL
        mpesa_api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        
        # Your Credentials
        BUSINESS_SHORTCODE = "174379"  # Test shortcode
        PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"  
        CALLBACK_URL = "https://7bb2-41-139-135-45.ngrok-free.app/api/mpesa-callback/"  # Change this to a live URL

        # Generate Password
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}".encode()).decode()

        # Prepare STK Push Request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "BusinessShortCode": BUSINESS_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": BUSINESS_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": CALLBACK_URL,
            "AccountReference": plan_name,
            "TransactionDesc": f"Subscription to {plan_name}"
        }

        print("Sending STK Push Request...")  # Debugging Print 8
        response = requests.post(mpesa_api_url, headers=headers, json=payload)

        print(f"STK Push Response Status Code: {response.status_code}")  # Debugging Print 9
        print(f"STK Push Response Body: {response.text}")  # Debugging Print 10

        if response.status_code == 200:
            response_data = response.json()
            checkout_request_id = response_data.get("CheckoutRequestID")

            if not checkout_request_id:
                print("No CheckoutRequestID received from M-Pesa.")  # Debugging Print
                transaction.status = "Failed"
                transaction.save()
                return JsonResponse({"status": "error", "message": "M-Pesa response did not contain CheckoutRequestID"})

            transaction.checkout_request_id = checkout_request_id  # Save CheckoutRequestID
            transaction.save()
            
            print(f"STK Push sent successfully. CheckoutRequestID: {checkout_request_id}")  # Debugging Print
            return JsonResponse({"status": "success", "message": "STK push sent successfully"})


            print("Invalid request method.")  # Debugging Print 11
            return JsonResponse({"status": "error", "message": "Invalid request"}, status=400)




def get_mpesa_access_token():
    import requests
    import json

    consumer_key = "v1WJvv47zBpXIGosa69XkPNHcHRKe8GaRCI2wqU6PEGZNDUF"  # Replace with your actual key
    consumer_secret = "XHX533TLzFBgSLTSiprNPYZYJ6mCd4UY1mXbSUpv0SRMzvEnKgZCwoNCHIrzfQrG"  # Replace with your actual secret

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(consumer_key, consumer_secret))
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None




@csrf_exempt
def mpesa_callback(request):
    print("M-Pesa Callback received.")  # Debugging Print
    
    try:
        data = json.loads(request.body)
        print(f"Callback Data: {data}")  # Debugging Print

        result_code = data["Body"]["stkCallback"]["ResultCode"]
        checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]
        
        # Find the transaction by checkout_request_id
        transaction = MpesaTransaction.objects.filter(checkout_request_id=checkout_request_id).first()

        if transaction:
            if result_code == 0:
                transaction.status = "Completed"
                print("Payment successful!")  # Debugging Print
            else:
                transaction.status = "Failed"
                print("Payment failed!")  # Debugging Print

            transaction.save()
            return JsonResponse({"status": "success"})
        else:
            print("Transaction not found.")  # Debugging Print
            return JsonResponse({"status": "error", "message": "Transaction not found"})
    
    except Exception as e:
        print(f"Error in callback processing: {str(e)}")  # Debugging Print
        return JsonResponse({"status": "error", "message": "Invalid callback data"})
