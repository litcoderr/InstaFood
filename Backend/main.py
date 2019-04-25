from flask import Flask, render_template, request, jsonify
from instagram_api import api
import time

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

api = api.API()

@app.route("/")
def root():
    return render_template("root.html")

@app.route("/show/", methods=['GET'])
def result():
    if request.method == 'GET': # Got response
        request_id = hash(time.time()) # unique request id
        query = request.args.get("query") # Get request query

        api.get(request_id, query) # start fetching thread
        return render_template("result.html", request_id=request_id)
    else:
        return render_template("root.html")

def generate_response(request_id):
    response = []
    print(request_id)
    if request_id in api.task:
        if not api.task[request_id]["is_running"]: # check for request id, if done
            response.append({"valid" : True})
            # iterate through responses
            # TODO Generate response api
        else: # not done
            response.append({"valid" : False})
    else:
        response.append({"valid" : False})
    return response

@app.route("/api/fetch/", methods=['GET'])
def fetch(): # function to call when checking for finished tasks
    if request.method == 'GET':
        request_id = int(request.args.get("request_id"))
        response = generate_response(request_id)
        return jsonify(response)
    else: # Not a get request
        pass

if __name__ == '__main__':
    app.run(debug=True)
