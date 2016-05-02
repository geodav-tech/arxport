def export(mxd_path, uid):
	'''Exports MXD specified by mxd_path to output folder specified below.
	UID must be passed from arxport.py.  Posts results of operation back 
	to server (this could probably be done more efficiently).'''

	import requests
	import arcpy
	import os

	try:
		map_doc = arcpy.mapping.MapDocument(mxd_path)
		folder = r'C:\path\to\your\arxport\static\output' # either hardcode this path or use os.getcwd()
		out_path = os.path.join(folder, os.path.basename(mxd_path[:-4])+'.pdf')
		arcpy.mapping.ExportToPDF(map_doc, out_path, resolution = '600', image_compression = 'LZW')
		status = 'complete'
		output = 'static/output/' + os.path.basename(mxd_path[:-4])+'.pdf'
	except Exception as e:
		status = e
		output = None

	# Post the results of the map export to the tasks output
	p = {'uid': uid, 'task_status': status, 'output': output}
	r = requests.post('http://localhost:5000/tasks/recent', params = p)
