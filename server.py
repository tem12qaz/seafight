import json

from flask import Flask, request

app = Flask(__name__)

users_state


@app.route('/', methods=['GET', 'POST'])
def main():
    if request.method == 'POST':

        body = json.loads(request.data)
        return json.dumps({'screen': body})
    else:
        return json.dumps({'screen': 'body'})


if __name__ == '__main__':
    app.run()
