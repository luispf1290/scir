/*$(document).ready(function() {
	// body.... id_serv_turno, id_serv_recol
	$("select[name=id_serv_area]").change(function(){
		alert($('select[name=id_serv_area]').val());
	});

	$("select[name=id_serv_turno]").change(function () {
		// body...
		alert($('select[name=id_serv_turno]').val());
	});

	$("select[name=id_serv_recol]").change(function () {
		// body...
		alert($('select[name=id_serv_recol]').val());
	});
	
});*/


$("select[name=id_serv_recol]").change(function () {
	
	var area = $('select[name=id_serv_area]').val();
	var turno = $('select[name=id_serv_turno]').val();
	var recol = $('select[name=id_serv_recol]').val();

	$.ajax({
		url: '/ajax/solicitud/',
		type: 'GET',
		dataType: 'json',
		data: {area:area, turno:turno, recol:recol, },

		success: function(datos){
			console.log(datos);
		} 

	});
		/*.done(function() {
			console.log("success");
		})
		.fail(function() {
			console.log("error");
		})
		.always(function() {
			console.log("complete");
		});*/
		
});
