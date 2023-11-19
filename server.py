from flask import Flask, request, jsonify
import json

app = Flask(__name__)
@app.route('/register', methods=['POST'])
def register():
    pass

@app.route('/login', methods=['POST'])
def login():
    pass

if __name__ == "__main__":
    body = request.data
    plain_body = len(body)
    data = json.loads(plain_body)


    app.run()