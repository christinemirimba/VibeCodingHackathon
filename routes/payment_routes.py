import os
import requests
from flask import Blueprint, request
from flask_restx import Namespace, Resource
from models import db, User, Transaction
from http import HTTPStatus

# Create a Blueprint and a Namespace
payment_bp = Namespace('payments', description='Payment processing via IntaSend')

# API credentials from environment variables
INTASEND_API_KEY = os.getenv('INTASEND_API_KEY')
INTASEND_API_BASE_URL = 'https://sandbox.intasend.com/api/v1' # Use sandbox for testing

@payment_bp.route('/initiate')
class PaymentInitiator(Resource):
    def post(self):
        """Initiates an IntaSend payment request."""
        data = request.get_json()
        email = data.get('email')
        phone = data.get('phone')
        amount = 100 # KES 100 for premium recipes
        
        if not email or not phone:
            return {'message': 'Email and phone number are required'}, HTTPStatus.BAD_REQUEST

        try:
            payload = {
                'api_key': INTASEND_API_KEY,
                'currency': 'KES',
                'amount': amount,
                'channel': 'MPESA_STK_PUSH',
                'customer': {
                    'email': email,
                    'phone': phone
                },
                'callback_url': os.getenv('INTASEND_CALLBACK_URL')
            }
            
            headers = {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            }
            
            response = requests.post(f'{INTASEND_API_BASE_URL}/payments', json=payload, headers=headers)
            response.raise_for_status()
            
            intasend_response = response.json()
            
            # Log the transaction in the database
            # For a real application, you'd associate this with a user
            # and a unique transaction ID from IntaSend.
            
            return intasend_response, HTTPStatus.OK
            
        except requests.exceptions.RequestException as e:
            return {'message': f'Payment initiation failed: {str(e)}'}, HTTPStatus.INTERNAL_SERVER_ERROR

@payment_bp.route('/callback')
class PaymentCallback(Resource):
    def post(self):
        """Receives and processes the payment status from IntaSend."""
        data = request.get_json()
        transaction_id = data.get('transaction_id')
        status = data.get('status')
        
        if status == 'SUCCESS':
            # This is where you would update the user's status to premium
            # For this example, we will just log it.
            print(f"Payment for transaction {transaction_id} was successful. User can be upgraded.")
            
        return {'message': 'Callback received'}, HTTPStatus.OK
