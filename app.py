"""
This module defines a Flask web application that provides APIs for various functionalities.
It includes routes to handle tree purchases via the Ecologi API and sending emails.

Routes:
- /purchase-trees (POST): Forwards tree purchase requests to the Ecologi API.
- /send-email (POST): Sends an email with provided details.
"""

import smtplib
from smtplib import SMTPException
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/purchase-trees', methods=['POST'])
def purchase_trees():
    """
    Handles the POST request to purchase trees.
    Forwards the request to the Ecologi API and returns the response.
    """
    print("Received request data:", request.json)  # Add this line to log the incoming data

    ecologi_api_url = 'https://public.ecologi.com/impact/trees'
    headers = {
        'Authorization': request.headers.get('Authorization'),
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(ecologi_api_url, headers=headers, json=request.json, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.Timeout:
        # Handle timeout exception
        return jsonify({'message': 'Request to Ecologi API timed out'}), 504
    except requests.RequestException as e:
        # Handle other request-related errors
        return jsonify({'message': f'An error occurred: {e}'}), 500

@app.route('/send-email', methods=['POST'])
def send_email():
    """
    Handles the POST request to send an email.
    Sends an email with the provided subject and body to the specified recipient.
    """
    data = request.json
    recipient_email = "joshsparkes6@gmail.com"
    sender_email = "joshsparkes6@gmail.com"
    sender_password = "dmdo vwry dukk cstf"

    # Set up the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = data['subject']

    # Add the email body
    body = data['body']
    msg.attach(MIMEText(body, 'plain'))

    # Set up the SMTP server
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        return jsonify({'message': 'Email sent successfully'}), 200
    except SMTPException as e:
        print(f"SMTP error occurred: {e}")
        return jsonify({'message': 'Failed to send email'}), 500

if __name__ == '__main__':
    app.run(debug=True)
