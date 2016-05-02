from flask import Flask, request, jsonify
from scripts import export_MXD
import threading
import uuid

app = Flask(__name__, static_url_path='')
app.debug = False  # ensure this is set to false when moving to production
tasks = {} # in-memory storage of recent tasks, will be cleared on script exit

# Return index.html when navigating to /
@app.route('/')
def root():
	return app.send_static_file('index.html')

# Returns the output PDF when called by name (including extension)
@app.route('/static/output/<filename>')
def send_map(filename):
	return app.send_static_file('output/{}'.format(filename))

# If GET, returns a JSON of recently processed tasks
# If POST with {'uid': '', 'task_status': '', 'output': ''}, adds task to JSON and returns JSON
@app.route('/tasks/recent', methods = ['GET', 'POST'])
def recent_tasks():
	if request.method == 'POST':
		tasks[request.args.get('uid')] = {'task_status': request.args.get('task_status'), 'output': request.args.get('output')}
	return jsonify(tasks)

# Returns JSON with output path/status for a specific task UID
@app.route('/tasks/<uid>', methods = ['GET'])
def recent_task_by_id(uid):
	if uid in tasks.keys():
		return jsonify(tasks[uid])
	else:
		return 'No tasks exist with that uid.'

# Exports an MXD on the server when passed with query string ?MXD_path=c:/esri/example.mxd
# MXD must be accessible by the computer running this script or it will error out
@app.route('/tasks/export_map', methods = ['GET'])
def export_map():
	if request.args.get('MXD_path'):
		uid = uuid.uuid4() # Generate unique ID
		export = threading.Thread(target= export_MXD.export, args=(request.args.get('MXD_path'),uid))
		export.start()  # Start map export in a new thread
	else:
		return 'You must specify an MXD path in your query string.  Ex: ?MXD_path=c:/esri/example.mxd'

	return jsonify({'uid': uid, 'task_status': 'processing', 'output': None})

if __name__ == '__main__':
	app.run(host='0.0.0.0')
