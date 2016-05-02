function mxdExport() {
	var mxdPath = $('#MXD').val();
	var uid;

	$('#message').text('processing');

	$.ajax({
	    url: 'http://localhost:5000/tasks/export_map',
	    data: {'MXD_path': mxdPath},
	    success: function(response) {
	        uid = response.uid;
	        $('#message').text(response.task_status);
	        checker();
	    }
	});

	function checker(){
		$.ajax({
		    url: 'http://localhost:5000/tasks/' + uid, 
		    complete: function(response) {
		    	console.log(response);
		    	if (response.responseText == 'No tasks exist with that uid.') {
		    		// Schedule the next request when the current one's complete
		    		setTimeout(checker, 5000);
		    	} else {
		    		$('#message').text(response.responseJSON.task_status);
		    		if (response.responseJSON.output){
		    			window.open('http://localhost:5000/'+response.responseJSON.output);
		    		}
		    	}
		    }
		});
	}
}