"""
A runthrough of the Facebook case study found in the
MAC x Learn | Flask workshop.

Note that each part is numbered in its order
of introduction in the workshop

Author: Jordan Zdimirovic (MAC)
"""

# Import Flask dependencies
from copy import deepcopy
from flask import Flask, jsonify, request


''' 1. Create a Flask app

    We typically use __name__ for identification
    If we run this file directly: __name__ == "__main__"
    Hence, this server will be the main server (by name)
'''

app = Flask(__name__) # Typically called "app"

''' 3. Add a Route

    We typically use __name__ for identification
    If we run this file directly: __name__ == "__main__"
    Hence, this server will be the main server (by name)
'''

# Let's create some friends to serve up
INITIAL_FRIENDS = [
    {
        "name": "John B",
        "age": 24,
        "workplace": "Monash University"    
    },
    {
        "name": "Michael S",
        "age": 22,
        "workplace": "Atlassian"    
    },
    {
        "name": "Rebecca H",
        "age": 19,
        "workplace": "Macquarie Bank"    
    },
    {
        "name": "Chloe W",
        "age": 26,
        "workplace": "Microsoft"    
    }
]

friends = deepcopy(INITIAL_FRIENDS) # Create a deep copy

# This 'decorator' defines a new route
# methods=["GET"] is default
@app.route("/friends/get", methods=["GET"])
def get_friends():
    # Print friends
    print(friends)
   
    # Return the list of friends
    return jsonify(friends)


@app.route("/friends/add", methods=["POST"])
def add_friend():
    # Get data from request
    request_data = request.json
    
    # Extract the "friend" instance
    new_friend = request_data['friend']
    
    # Add to data store
    friends.append(new_friend)
    
    # Return response
    return f"Successfully added friend: [{new_friend['name']}]", 200 # OK!


# Parameter converters: int, string, float
@app.route("/friends/delete/<int:idx>", methods=["DELETE"])
def del_friend(idx: int):
    # If not in range then tell the client it was a bad request
    if not (0 <= idx < len(friends)):
        return jsonify({
            "message": "Index out of range / not found"
        }), 404
    
    # We're safe to pop from friends at position idx
    deleted_friend = friends.pop(idx)
    
    return jsonify({
        "message": "Successfully deleted",
        "friend": deleted_friend 
    }), 200

''' 2. Serve / run a Flask app

    We have two options here:
    - Only open to localhost
    - Open on your LAN IP (required)
    
    We do the latter so we can interact with others in the workshop
'''

app.run("0.0.0.0", 80)
