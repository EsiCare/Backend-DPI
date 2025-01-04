from flask import Flask, request, jsonify
import random
import requests

app = Flask(__name__)
esicare_server_endpoint = "http://localhost:8000/api/prescriptions"

@app.route('/api/prescriptions', methods=['GET'])
def get_prescriptions():
    params = request.args
    try:
        response = requests.get(esicare_server_endpoint, params=params)
        response.raise_for_status()  # Raise exception for HTTP errors

        return jsonify({
            "status": "success",
            "data": response.json()["data"]
        }), 200
    except requests.RequestException as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/api/prescriptions/update/<int:pk>', methods=['POST'])
def validate_prescription(pk):

    endpoint = esicare_server_endpoint + f"/update/{pk}"
    
    outgoing_data = {**request.get_json()}

    try:
        # Send a POST request to the external server
        response = requests.post(endpoint, json=outgoing_data)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Return the response from the external server
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
