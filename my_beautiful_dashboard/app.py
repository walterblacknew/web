from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# In-memory list to store incoming webhook data (for demonstration)
ALL_RESPONSES = []

@app.route("/webhook", methods=["POST"])
def porsline_webhook():
    """
    Webhook endpoint that Porsline will POST to
    whenever a new response (or event) occurs.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    
    # Append the incoming data to our in-memory list
    ALL_RESPONSES.append(data)
    
    # Return a success response to Porsline
    return jsonify({"status": "ok"}), 200

@app.route("/dashboard", methods=["GET"])
def dashboard():
    """
    A beautiful dashboard displaying the collected responses 
    in a searchable, filterable table (using DataTables).
    """
    return render_template("dashboard.html", responses=ALL_RESPONSES)

@app.route("/", methods=["GET", "POST"])
def index():
    """
    Root route:
    - GET: simple welcome page with a link to /dashboard
    - POST: now allowed, so we won't get a 405 if a POST request is sent here
    """
    if request.method == "POST":
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON provided"}), 400
        
        # You can decide what to do with POST data at the root.
        # For now, just return it back as a JSON response.
        return jsonify({"status": "Data received at root", "data": data}), 200
    else:
        return '''
        <h2>Welcome to the Beautiful Dashboard</h2>
        <p>برای مشاهده‌ی داشبورد <a href="/dashboard">کلیک کنید</a>.</p>
        '''

if __name__ == "__main__":
    # Run on the Flask development server with debug mode
    app.run(debug=True, host="0.0.0.0", port=5000)
