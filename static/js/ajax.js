$(".buton-modal").click(function () {
  /* Act on the event */
  var id = $(this).val();
  $.ajax({
      url: '/insumos/insumo/detalle/',
      type: 'GET',
      dataType: 'json',
      data: {
        id: id
      },

      success: function (datos) {
        console.log(datos);
        var html = "";
        for (var i = 0; i < datos.length; i++) {
          html += "<div class='modal-header'>" +
            "<h5 class'modal-title'>" + datos[i].fields.nombre + "</h5>" +
            "<button type='button' class='close' data-dismiss='modal' aria-label='Close'>" +
            "<span aria-hiden='true'>&times;</span>" +
            "</button>" +
            "</div>" +
            "<div class='modal-body'>" +
            "<h4 class='center'>" + datos[i].fields.uso + "</h4>" +
            "<h4 class='center'>" + datos[i].fields.presentacion + "ml</h3>" +
            "<h4 Class='center'>" + datos[i].fields.unidades + "unidades</h3>" +
            "</div>" +
            "<div class=' modal-footer'>"+
            "<button type='button' class=' btn btn-block btn-danger' data-dismiss='modal' >Cerrar</button>"+
            "</div>";

        }
        $('#datos').html(html);
      }
    })
    .done(function () {
      console.log("success");
    })
    .fail(function () {
      console.log("error");
    })
    .always(function () {
      console.log("complete");
    });

});