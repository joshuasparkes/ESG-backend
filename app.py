from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

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

if __name__ == '__main__':
    app.run(debug=True)
