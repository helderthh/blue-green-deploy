from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/ping')
def handle_ping():
    return 'pong'

@app.route('/healthz')
def handle_healthz():
    resp = jsonify(success=True)
    return resp

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8001)
