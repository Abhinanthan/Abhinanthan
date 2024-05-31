from flask import Flask, request, jsonify
import json

app = Flask(__name__)

@app.route('/receive', methods=['POST'])
def receive_data():
    try:
        # Get the JSON data from the request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        # Process the data (this is where you handle the received data)
        # For example, let's just print it out
        print("Received data:", json.dumps(data, indent=4))

        # Send a success response back to the sender
        return jsonify({"message": "Data received successfully"}), 200
    
    except Exception as e:
        # Handle any exceptions and send an error response
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)