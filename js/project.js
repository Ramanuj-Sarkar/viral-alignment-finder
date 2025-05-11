// run gene_finder.cgi or show an error
function runSearch( term ) {
	// hide and clear the previous results, if any
	$('#results').hide();
	$('tbody').empty();
        $('#header').empty();


	// transforms all the form parameters into a string we can send to the server
	var frmStr = $('#gene_choice').serialize();
	frmStr += "&" + $('#column_choice').serialize();

	$.ajax({
		url: './gene_finder.cgi',
		type: 'POST',
		dataType: 'json',
		data: frmStr,
		success: function(data, textStatus, jqXHR) {
			processSearchJSON(data);
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert("Failed to perform gene search! textStatus: (" + textStatus +
				") and errorThrown: (" + errorThrown + ")");
		}
	});
}

// change the way gene_finder.html looks based on the cgi
function processSearchJSON( data ) {
	
	if( data.misc.cols == 0 ) {
		$('#match_count').text( '0' );
	}
	else {
                $('#match_count').text( data.match_count );
	}
	
	// add the headers
	if(data.columns.organism == "yes"){
		$('<td/>', { text : "Organism" } ).appendTo('#header');
	}
	
	if(data.columns.genename == "yes"){
                $('<td/>', { text : "Gene Name" } ).appendTo('#header');
        }
	
        if(data.columns.productname == "yes"){
                $('<td/>', { text : "Product Name" } ).appendTo('#header');
        }

        if(data.columns.length == "yes"){
                $('<td/>', { text : "Length" } ).appendTo('#header');
        }
	

	// this will be used to keep track of row identifiers
	var next_row_num = 1;

	// iterate over each match and add a row to the result table for each
	$.each( data.matches, function(i, item) {
		var this_row_id = 'result_row_' + next_row_num++;

		// create a row and append it to the body of the table
		$('<tr/>', { "id" : this_row_id } ).appendTo('tbody');

		// add the columns
                if(data.columns.organism == "yes"){
                        $('<td/>', { "text" : item.organism} ).appendTo('#' + this_row_id);
                }		

                if(data.columns.genename == "yes"){
                        $('<td/>', { "text" : item.genename } ).appendTo('#' + this_row_id);
                }

                if(data.columns.productname == "yes"){
                        $('<td/>', { "text" : item.productname } ).appendTo('#' + this_row_id);
                }		

        	if(data.columns.length == "yes"){		
                	$('<td/>', { "text" : item.length } ).appendTo('#' + this_row_id);
		}

	});
	
	// now show the result section that was previously hidden
	$('#results').show();
}

// run alignment_finder.cgi or show an error
function runAlignment( term ) {
        // hide and clear the previous results, if any
        $('#alignment_results').hide();
	
        // transforms all the form parameters into a string we can send to the server
        var frmStr = $('#alignment_data').serialize();

        $.ajax({
                url: './alignment_finder.cgi',
                type: 'POST',
                dataType: 'json',
                data: frmStr,
                success: function(data, textStatus, jqXHR) {
                        processAlignmentJSON(data);
                },
                error: function(jqXHR, textStatus, errorThrown){
                        alert("Failed to perform gene search! textStatus: (" + textStatus +
                                ") and errorThrown: (" + errorThrown + ")");
                }
        });
}

function processAlignmentJSON( data ) {
	if (data.error == 'No errors detected.') {
		$('#alignment_count').text( data.align_count );
        	$('#alignment_score').text( data.align_score );
                $('#alignment').text( data.align );
		$('#alignment_results').show();
	} else {
	        alert( data.error );
	}
}

// run our javascript once the page is ready
$(document).ready( function() {
	// gene submission form
	$('#submit').click( function() {
		runSearch();
        	return false;  // prevents 'normal' form submission
	});

	// alignment submission form
        $('#submit_alignment').click( function() {
                runAlignment();
                return false;
        });
});
