from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api/', methods=['GET', 'POST'])
def add_message():
    content = request.json
    print (content)
    return '{"status": 200}\n'

if __name__ == '__main__':
    app.run(host= '0.0.0.0',port=105)