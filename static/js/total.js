ids = ["sumar", "sumar2", "sumar3", "sumar4", "sumar5",
		"sumar6", "sumar7", "sumar8", "sumar9", "sumar10",
		"sumar11", "sumar12", "sumar13", "sumar14", "sumar15",
		"sumar16", "sumar17", "sumar18", "sumar19", "sumar20",
		"sumar21", "sumar22", "sumar23", "sumar24", "sumar25"];

ids2 = ["sumar26", "sumar27", "sumar28", "sumar29", "sumar30",
		"sumar31", "sumar32", "sumar33", "sumar34", "sumar35",
		"sumar36", "sumar37", "sumar38", "sumar39", "sumar40",
		"sumar41", "sumar42", "sumar43", "sumar44", "sumar45",
		"sumar46", "sumar47", "sumar48", "sumar49", "sumar50"];

lavs = ["id_lav_sabana", "id_lav_colcha", "id_lav_funda", "id_lav_pantalon_pij", "id_lav_camisa_pij",
		"id_lav_camison", "id_lav_cobertor", "id_lav_bataquir", "id_lav_cd_120", "id_lav_cd_80",
		"id_lav_cd_40", "id_lav_cs_120", "id_lav_cs_80", "id_lav_pantalon_cs_40", "id_lav_fun_mayo",
		"id_lav_comp_raquia", "id_lav_saco_cir", "id_lav_pant_cir", "id_lav_sab_h", "id_lav_sab_r",
		"id_lav_sab_pie", "id_lav_bata", "id_lav_toalla", "id_lav_pij_inf", "id_lav_mantel"];

servs = ["id_serv_sabana", "id_serv_colcha", "id_serv_funda", "id_serv_pantalon_pij", "id_serv_camisa_pij",
		"id_serv_camison", "id_serv_cobertor", "id_serv_bataquir", "id_serv_cd_120", "id_serv_cd_80",
		"id_serv_cd_40", "id_serv_cs_120", "id_serv_cs_80", "id_serv_pantalon_cs_40", "id_serv_fun_mayo",
		"id_serv_comp_raquia", "id_serv_saco_cir", "id_serv_pant_cir", "id_serv_sab_h", "id_serv_sab_r",
		"id_serv_sab_pie", "id_serv_bata", "id_serv_toalla", "id_serv_pij_inf", "id_serv_mantel"];

var lav = "";
var serv = "";

function manejadorCallback(evento) {
	// body...
	alert(evento.target.id);

	for (var i = 0; i < ids.length.length; i++) {
		if (evento.target.id) {
			for (var i = 0; i < lavs.length; i++) {
				lav = document.getElementById(lavs[i]).value;
				lav = parseInt(lav);
				lav = lav + 1;
				document.getElementById(lavs[i]).value = lav;
			}

			alert(ids[i]);		
		}else{
			alert("no funciona");	
		}
		
	}

}


var buttons = document.querySelectorAll('.btn-contador');
for (var i = 0 ; i < buttons.length; i++) {
	buttons[i].addEventListener('click', manejadorCallback);
}