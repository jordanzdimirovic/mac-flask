# Create Flask server
from flask import Flask, jsonify, request

from ttshelper import say

import os

DATA_FILENAME = "data.txt"

app = Flask(__name__)

# Create routes
@app.route("/say", methods=["POST"])
def say_endpoint():
    # Get request json
    to_say = request.json['message']
    
    if to_say == "":
        return "Your message was empty", 400
    
    # Say using tts helper
    say(to_say)
    
    return f"Successfully said {to_say}", 200


@app.route("/write_line", methods=["POST"])
def writeline():
    # Check if file exists - if not, create it
    file_method = "a" if os.path.exists(DATA_FILENAME) else "x"
    
    # Get request json
    line = request.json['line']
    
    # Open file and append with newline for next time
    with open(DATA_FILENAME, file_method) as f:
        f.write(line + "\n")
        
    return f"Successfully wrote line '{line}'", 200
    

@app.route("/get_lines", methods=["GET"])
def getlines():
    # Check if file exists - if not, send back empty list
    if not os.path.exists(DATA_FILENAME):
        return jsonify([]), 200
    
    # Open file in regular read mode
    with open(DATA_FILENAME, 'r') as f:
        # Get rid of new lines / whitespace when returning lines
        all_lines = [line.strip() for line in f.readlines()]
    
    return jsonify(all_lines), 200
    

@app.route("/get_lines/<int:line_no>", methods=["GET"])
def get_line_with_id(line_no: int):
    # Check if file exists - if not, any number is invalid
    if not os.path.exists(DATA_FILENAME):
        return f"There is no line with number {line_no}", 404
    
    # Open file in regular read mode
    with open(DATA_FILENAME, 'r') as f:
        all_lines = f.readlines()
        
    # Check if number in bounds
    if not (0 <= line_no < len(all_lines)):
        return f"There is no line with number {line_no}", 404
    
    # Get rid of new lines / whitespace
    return all_lines[line_no].strip(), 200


# Run on all IPs
app.run("0.0.0.0", 81, threaded=False)
