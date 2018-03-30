from flask import (Flask, jsonify, request)

from extractor import extract

app = Flask(__name__)


@app.route('/')
def index():
    return """
    <form action="/extract">
        <input type="text" name="url" placeholder="Enter a URL" />
        <button type="submit">Submit</button>
    </form>
    """


@app.route('/extract')
def extract_url():
    url = request.args.get('url', '')
    if not url:
        return jsonify(type='error', result='Provide a URL'), 406
    return jsonify(type='success', result=extract(url))


if __name__ == '__main__':
    app.run(debug=True, port=5000)