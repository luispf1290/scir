
function mult() {

  var total = 0;
  var prueba = 3;
  
  $(".monto").each(function() {

    if (isNaN(parseFloat($(this).val()))) {

      total += 0;

    } else {

      total = parseFloat($(this).val()) * parseFloat($('#id_unidades').val());

    }

  });
  //alert(total);
  document.getElementById('id_total').value = total;

}