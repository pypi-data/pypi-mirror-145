from flask import Flask,abort, current_app, request, url_for,jsonify,make_response
from werkzeug.exceptions import HTTPException, InternalServerError
from flask_restful import Resource, Api
from datetime import datetime
from functools import wraps
import threading
import time
import uuid
from merakitools.main import run
from os import getenv


tasks = {}

app = Flask(__name__)
api = Api(app)


@app.before_first_request
def before_first_request():
    """Start a background thread that cleans up old tasks."""
    def clean_old_tasks():
        """
        This function cleans up old tasks from our in-memory data structure.
        """
        global tasks
        while True:
            # Only keep tasks that are running or that finished less than 5
            # minutes ago.
            five_min_ago = datetime.timestamp(datetime.utcnow()) - 5 * 60
            tasks = {task_id: task for task_id, task in tasks.items()
                     if 'completion_timestamp' not in task or task['completion_timestamp'] > five_min_ago}
            time.sleep(60)

    if not current_app.config['TESTING']:
        thread = threading.Thread(target=clean_old_tasks)
        thread.start()


def async_api(wrapped_function):
    @wraps(wrapped_function)
    def new_function(*args, **kwargs):
        def task_call(flask_app, environ):
            # Create a request context similar to that of the original request
            # so that the task can have access to flask.g, flask.request, etc.
            with flask_app.request_context(environ):
                try:
                    tasks[task_id]['return_value'] = wrapped_function(*args, **kwargs)
                except HTTPException as e:
                    tasks[task_id]['return_value'] = current_app.handle_http_exception(e)
                except Exception as e:
                    # The function raised an exception, so we set a 500 error
                    tasks[task_id]['return_value'] = InternalServerError()
                    if current_app.debug:
                        # We want to find out if something happened so reraise
                        raise
                finally:
                    # We record the time of the response, to help in garbage
                    # collecting old tasks
                    tasks[task_id]['completion_timestamp'] = datetime.timestamp(datetime.utcnow())

                    # close the database session (if any)

        # Assign an id to the asynchronous task
        task_id = uuid.uuid4().hex

        # Record the task, and then launch it
        tasks[task_id] = {'task_thread': threading.Thread(
            target=task_call, args=(current_app._get_current_object(),
                               request.environ))}
        tasks[task_id]['task_thread'].start()

        # Return a 202 response, with a link that the client can use to
        # obtain task status
        print(url_for('gettaskstatus', task_id=task_id))
        #return jsonify()f"ccepted location {url_for('gettaskstatus', task_id=task_id)}", 202, {'Location': url_for('gettaskstatus', task_id=task_id)}
        return make_response(jsonify({"message": "Proccess Accepted",
                                      "status": 202,
                                      "status url": url_for('gettaskstatus', task_id=task_id)}),
                             202,
                             {'Location': url_for('gettaskstatus', task_id=task_id)})
    return new_function


class GetTaskStatus(Resource):
    def get(self, task_id):
        """
        Return status about an asynchronous task. If this request returns a 202
        status code, it means that task hasn't finished yet. Else, the response
        from the task is returned.
        """
        task = tasks.get(task_id)
        if task is None:
            abort(404)
        if 'return_value' not in task:
            #return "Sync Still Running", 202, {'Location': url_for('gettaskstatus', task_id=task_id)}
            return make_response(jsonify({"message" : "Sync Still Running",
                                          "status" : 202,
                                          "status url": url_for(
                                              'gettaskstatus',
                                              task_id=task_id)}),
                                 202,
                                 {'Location': url_for('gettaskstatus',
                                                      task_id=task_id)})
        return make_response(jsonify({"message" : "Sync Complete",
                                          "status" : 200}),
                                 202)


class CatchAll(Resource):
    @async_api
    def get(self, path=''):
        # perform some intensive processing
        print("starting processing task, path: '%s'" % path)
        time.sleep(10)
        print("completed processing task, path: '%s'" % path)
        return f'The answer is: {path}'

class Sync(Resource):
    @async_api
    def get(self, path=''):
        # perform some intensive processing
        config_file = getenv("MERAKI_TOOLS_CONFIG", None)
        if config_file is None:
            return "No Config Filed Defined"
        run(config_file,task='sync',network_name="29Q892,09X055,07X018,15B029,15B094,02M041")
        #run(config_file, task='sync')
        print("starting processing task, path: '%s'" % path)
        time.sleep(10)
        print("completed processing task, path: '%s'" % path)
        return f'The answer is: {path}'

api.add_resource(CatchAll, '/<path:path>', '/')
api.add_resource(GetTaskStatus, '/status/<task_id>')
api.add_resource(Sync,'/sync')


if __name__ == '__main__':
    app.run(debug=True)