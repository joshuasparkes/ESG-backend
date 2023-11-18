from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

@app.route('/purchase-trees', methods=['POST'])
def purchase_trees():
    print("Received request data:", request.json)  # Add this line to log the incoming data

    ecologi_api_url = 'https://public.ecologi.com/impact/trees'
    headers = {
        'Authorization': request.headers.get('Authorization'),
        'Content-Type': 'application/json'
    }

    # Forward the POST request to the Ecologi API
    response = requests.post(ecologi_api_url, headers=headers, json=request.json)

    # Return the response from the Ecologi API
    return jsonify(response.json()), response.status_code

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    recipient_email = "joshsparkes6@gmail.com"  # Your email
    sender_email = "joshsparkes6@gmail.com"     # Replace with your email
    sender_password = "dmdo vwry dukk cstf"           # Replace with your email password

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
    except Exception as e:
        print(e)
        return jsonify({'message': 'Failed to send email'}), 500

if __name__ == '__main__':
    app.run(debug=True)
