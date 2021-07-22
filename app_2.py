import datetime
import os

import requests
from flask import Flask, request, current_app, send_from_directory, jsonify

from VariantClassification import runVariantClassification

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue
import tempfile

tasks = Queue()

executors = {
    'default': ThreadPoolExecutor(1),
    'processpool': ProcessPoolExecutor(1)
}

sched = BackgroundScheduler(timezone='UTC', executors=executors)

def job():
    print("Hi")
    if not tasks.empty():
        task = tasks.get()
        try:
            execution_id = task.get("execution_id")
            step_id = task.get("step_id")
            filename = task.get("filename")
            print(execution_id)
            print(step_id)
            print(filename)
            url = "http://localhost:8080/api/v1/providers/{}/executions/{}/steps/{}".format(PROVIDER_ID, execution_id, step_id)
            headers = {}
            payload = {
                "status": "SUCCESS",
                "uri": "http://localhost:5002/v1/uploads/{}".format(filename)
            }
            response = requests.request("POST", url, json=payload, headers=headers, timeout=(3.05, 10))
            print(response.status_code)
            print(response.json())
        except Exception as error:
            print(error)
            return None


sched.add_job(job, 'interval', seconds=20)
sched.start()

app = Flask(__name__)
UPLOAD_FOLDER = './static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False


PROVIDER_ID = "49df4595-b8af-4e32-8791-65e583ae08a2"


@app.route('/v1/pipegine/provider/process', methods=['POST'])
def upload():
    execution_id = request.headers.get("x-pipegene-execution-id")
    step_id = request.headers.get("x-pipegene-step-id")


    file = tempfile.NamedTemporaryFile().name
    request.files['file'].save(file)


    columns_param = request.form.get("columns").split(',')
    columns = list(map(lambda s: s.strip(), columns_param))
    print(columns)

    # maf = read_maf(file, columns)
    date = datetime.datetime.now().isoformat()
    upload_dir = "{}/{}".format(app.config['UPLOAD_FOLDER'], date)
    result = runVariantClassification(file, upload_dir)

    tasks.put({
        "execution_id": execution_id,
        "step_id": step_id,
        "filename": result.replace("static/", "")
    })

    return jsonify({
        "urlToCheck": "http://localhost:5002/v1/pipegene/{}/status".format(step_id),
        "message": "IN_PROGRESS",
    })

@app.route('/v1/uploads/<path:filename>', methods=['GET'])
def download(filename):
    uploads = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    return send_from_directory(directory=uploads, filename=filename, )

@app.route('/', methods=['GET'])
def hello():
    return 'hello'

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5002)
