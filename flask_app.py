from flask import Flask


app = Flask(__name__)

@app.route('/')
def index():
  return requests.get('https://ya.ru').text

if __name__ == '__main__':
  app.run(threaded=True)
