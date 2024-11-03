# server.py

import time
import random
from flask import Flask, jsonify

app = Flask(__name__)

# Configurable delay in seconds (adjust as needed)
CONFIGURABLE_DELAY = random.randint(5, 15)

# Job start time
JOB_START_TIME = time.time()

# Simulated job status
JOB_STATUS = 'pending'

@app.route('/status', methods=['GET'])
def get_status():
    global JOB_STATUS
    elapsed_time = time.time() - JOB_START_TIME

    if elapsed_time >= CONFIGURABLE_DELAY and JOB_STATUS == 'pending':
        # After the delay, randomly set the status to 'completed' or 'error'
        JOB_STATUS = random.choice(['completed', 'error'])

    return jsonify({'result': JOB_STATUS})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
