import datetime
import os

import requests
from flask import Flask, request, current_app, send_from_directory, jsonify

from PreProcessamentoCompleto import runPreProcessamento

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from queue import Queue
import tempfile

PLATFORM_URL = os.getenv('PLATFORM_URL', "localhost")

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
            url = "http://{}:8080/api/v1/providers/{}/executions/{}/steps/{}".format(PLATFORM_URL, PROVIDER_ID, execution_id, step_id)
            headers = {}
            payload = {
                "status": "SUCCESS",
                "uri": "http://localhost:5011/v1/uploads/{}".format(filename)
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
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

PROVIDER_ID = "78cec5db-6396-4fd9-803f-1fd469d76312"
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# 
# A ideia desse serviço é receber um input e como output vai devolver um png
# com o resultado do pre processamento, esse serviço está salvo na base com
# PROVIDER_ID=78cec5db-6396-4fd9-803f-1fd469d76312
#
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
    output_file_name = "{}/BRCA2_data_mutations_extended-{}.maf".format(app.config['UPLOAD_FOLDER'], date)
    result = runPreProcessamento(file, columns, output_file_name, upload_dir)

    print("aobaaaaaaa")

    tasks.put({
        "execution_id": execution_id,
        "step_id": step_id,
        "filename": result.replace("static/", "")
    })

    return jsonify({
        "urlToCheck": "http://localhost:5011/v1/pipegene/{}/status".format(step_id),
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
    address = "0.0.0.0" if os.getenv('PLATFORM_URL') != None else "127.0.0.1"

    print(address)

    app.run(host=address, port=5011)
