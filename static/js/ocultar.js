function mostrar(opcion){
    if(opcion == 1){
        document.getElementById('anual').style.display="flex";
        document.getElementById('semestral').style.display="none";
        document.getElementById('trimestral').style.display=('none');
        document.getElementById('mensual').style.display="none";
        
    }else if(opcion == 2){
        document.getElementById('anual').style.display="none";
        document.getElementById('semestral').style.display="flex";
        document.getElementById('trimestral').style.display=('none');
        document.getElementById('mensual').style.display="none";
        
    } else if (opcion == 3){
        document.getElementById('trimestral').style.display=('flex');
         document.getElementById('anual').style.display="none";
         document.getElementById('semestral').style.display="none";
         document.getElementById('mensual').style.display="none";
        
    } else if(opcion == 4){
        document.getElementById('trimestral').style.display=('none');
         document.getElementById('anual').style.display="none";
         document.getElementById('semestral').style.display="none";
        document.getElementById('mensual').style.display="flex";
    }
}