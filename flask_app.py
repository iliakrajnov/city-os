from flask import Flask, send_file
from time import sleep, time, ctime
from threading import Thread
import requests


def record(url, res):
    global threads_data
    last = ''
    
    while threads_data[res][1]:
        filename = requests.get(url + 'live.m3u8').text.splitlines()[-1]
        if filename != last:
            last = filename
            with open(res, 'ab') as file:
                file.write(requests.get(url + filename).content)
        sleep(1)

#-------------------------------


app = Flask(__name__)
threads_data = {}


@app.route('/<place>')
def index(place):
    global threads_data
    try:
        threads_data[str(place)+'.ts'][1] = False
        threads_data[str(place)+'.ts'][0].join()
        del threads_data[str(place)+'.ts']
        return 'stopped at ' + ctime(time())

    except KeyError:
        thr = Thread(target=record, args=(f'https://webcam.sarbc.ru/{place}/hls/', str(place)+'.ts'))
        threads_data[str(place)+'.ts'] = [thr, True]
        thr.start()
        return 'started at ' + ctime(time())


@app.route('/get/<place>')
def get(place):
    return send_file(str(place)+'.ts')

if __name__ == '__main__':
    app.run()
