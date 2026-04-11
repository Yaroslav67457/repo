from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

server_cache = {"value": 0}
BIT_LENGTH = 8
PASSWORD = "123daN321@123"

def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Password'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.after_request
def after_request(response):
    return add_cors_headers(response)

@app.route('/controller_1.6')
def control_page():
    return render_template('control.html')

@app.route('/', methods=["GET", "POST", "OPTIONS"])
def main():
    if request.method == "OPTIONS":
        return jsonify({"status": "ok"}), 200

    if request.method == "POST":
        password = request.headers.get("Password")
        if password != PASSWORD:
            return jsonify({"error": "Unauthorized."}), 401

        binary_value = request.form.get("value")
        if binary_value and len(binary_value) == BIT_LENGTH and all(c in "01" for c in binary_value):
            server_cache["value"] = int(binary_value, 2)
            return jsonify({"value": format(server_cache["value"], f'0{BIT_LENGTH}b')}), 200

        return jsonify({"error": f"Invalid binary value."}), 400

    return jsonify({"value": format(server_cache["value"], f'0{BIT_LENGTH}b')}), 200