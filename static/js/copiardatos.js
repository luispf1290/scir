function copiarDatos(){

	var numeroSerie = document.getElementById("numeroserie").value;
	var referencia = document.getElementById("referencia").value;
	var peso = document.getElementById("peso").value;

	var texto = numeroSerie + "\t\t" + referencia + "\t\t" + peso;

	document.getElementById("textToEncode").innerHTML = texto;

}

// funcion con jquery

function pasardatos(){
	var numeroserie = $("#numeroserie").val();
	var referencia = $("#referencia").val();
	var peso = $("#peso").val();

	var datos = numeroserie+" "+referencia+" "+peso;

	$("#textToEncode").val(datos); 
}