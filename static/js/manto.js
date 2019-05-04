

//window.addEventListener('load', fechaActual);

$(document).ready(fechaActual);

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

                if (!data[0].fields.aplicado) {
                    var html="";
                    for (var i = 0; i < data.length; i++) {
                        console.log(data);
                        html += "<div class='modal-header'>" +
                        "<h5 class'modal-title'>" + data[i].fields.fecha + "</h5>" +
                        "<button type='button' class='close' data-dismiss='modal' aria-label='Close'>" +
                        "<span aria-hiden='true'>&times;</span>" +
                        "</button>" +
                        "</div>" +
                        "<div class='modal-body'>" +
                        "<h3 class='center'>" + data[i].fields.descripcion + "</h3>" +
                        "</div>" +
                        "<div class=' modal-footer'>"+
                        "<button type='button' class=' btn btn-block btn-danger' data-dismiss='modal' >Cerrar</button>"+
                        "</div>";
                        
                    }
                    $('#datos').html(html);
                    $("#manto").modal("show");
                    
                }
            },
            error: function(err) {
                
            }
        });
    }
