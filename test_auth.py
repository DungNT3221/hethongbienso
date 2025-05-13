from flask import Flask

app = Flask(__name__)

@app.route('/test')
def test():
    return 'Test successful!'

if __name__ == '__main__':
    print('Starting test server on port 3001...')
    app.run(host='0.0.0.0', port=3001, debug=True)
