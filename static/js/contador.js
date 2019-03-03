var lav = 0;
var serv = "";


for (let i = 0; i < 26; i++) {
	$('.btn-suma' + i).click(function (e) {
		lav = document.getElementById('id_solicitud_set-' + i + '-recibe_lav').value;
		lav = parseInt(lav);
		lav = lav + 1;
		document.getElementById('id_solicitud_set-' + i + '-recibe_lav').value = lav;
		document.getElementById('id_solicitud_set-' + i + '-total_lav').value = document.getElementById('id_solicitud_set-' + i + '-recibe_lav').value;
	});

	$('.btn-resta' + i).click(function (e) {
		lav = document.getElementById('id_solicitud_set-' + i + '-recibe_lav').value;
		lav = parseInt(lav);
		lav = lav - 1;
		document.getElementById('id_solicitud_set-' + i + '-recibe_lav').value = lav;
		document.getElementById('id_solicitud_set-' + i + '-total_lav').value = document.getElementById('id_solicitud_set-' + i + '-recibe_lav').value;
	});

	$('#btn-sumar' + i).click(function (e) {
		serv = document.getElementById('id_solicitud_set-' + i + '-recibe_serv').value;
		serv = parseInt(serv);
		serv = serv + 1;
		document.getElementById('id_solicitud_set-' + i + '-recibe_serv').value = serv;
		document.getElementById('id_solicitud_set-' + i + '-total_serv').value = document.getElementById('id_solicitud_set-' + i + '-recibe_serv').value;
	});

	$('#btn-restar' + i).click(function (e) {
		serv = document.getElementById('id_solicitud_set-' + i + '-recibe_serv').value;
		serv = parseInt(serv);
		serv = serv - 1;
		document.getElementById('id_solicitud_set-' + i + '-recibe_serv').value = serv;
		document.getElementById('id_solicitud_set-' + i + '-total_serv').value = document.getElementById('id_solicitud_set-' + i + '-recibe_serv').value;

	});
}

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

	document.getElementById("id_fecha").value = hoy;
}