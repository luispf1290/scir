

window.addEventListener('load', fechaActual, false);

function fechaActual() {
	// body...
	var hoy = new Date();
	var dd = hoy.getDate();
	var mm = hoy.getMonth() + 1; //hoy es 0!
	var yyyy = hoy.getFullYear();

	if (dd < 10) {
		dd = '0' + dd;
	}

	if (mm < 10) {
		mm = '0' + mm;
	}

    hoy = yyyy + '-' + mm + '-' + dd;
    

    $.ajax({
        type: "GET",
        url: "/fecha_manto/",
        data: {'fecha': hoy},
        dataType: "json",
        success: function (data) {
            alert(data[0].fields.fecha);
        },
        error: function(err) {
            
        }
    });
}