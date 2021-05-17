from flask import Flask

app = Flask(__name__)


@app.route('/', methods=['GET'])
def server_start():
    return "This is starting point for this server"



app.run(debug=True)