# arxport
This code sample shows how to structure a flask REST API that will call an arcpy script to allow a user to export Esri
Map Documents (MXDs) on the server remotely via the web.  

#### Dependencies
* Python 2.7
* Flask 0.10.1
* arcpy (I'm using the version that comes with ArcMap 10.2)
* requests 2.9.1

#### Setup
1. Ensure all dependencies are installed.
2. Change [this line](https://github.com/geodav-tech/arxport/blob/master/scripts/export_MXD.py#L12) to wherever your `arxport/static/output` folder ends up.
3. Change every instance of `localhost` in [this file](https://github.com/geodav-tech/arxport/blob/master/static/form_control.js) to the IP address of the server running arxport.py.  If you're just running this locally, nothing needs to change.
4. Run arxport.py and navigate to `http://localhost:5000` if you're on the same computer that's running arxport.py, or `http://<server_ip_address>:5000` if you're remote.

