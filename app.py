import flask
from flask import request
import json
from tasks_manager import start_task
from log_manager import get_logger

log = get_logger()

app = flask.Flask(__name__)


@app.route('/data_prep', methods=['POST'])
def task_handler():
    """
    :return:
    :Description: This is the entry point of the execution, This function will convert the user request
    to json and send it to task manager to start the execution. If User input is not a valid json then it will
    return invalid request
    """
    try:
        response = request.data
        response_json = json.loads(response.decode('utf-8'))
        return start_task(response_json)
    except Exception as e:
        log.error("Failed to parse user request" + str(e))
        return "Invalid Input Please check the input"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
