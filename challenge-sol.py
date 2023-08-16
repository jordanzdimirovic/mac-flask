# Create Flask server
from flask import Flask, jsonify, request

from ttshelper import say

app = Flask(__name__)

# Create routes
@app.route("/say", methods=["POST"])
def say_endpoint():
    # Get request json
    to_say = request.json['message']
    
    # Say using tts helper
    say(to_say)
    
    return f"Successfully said {to_say}"


# Run on all IPs
app.run("0.0.0.0", 81, threaded=False)
