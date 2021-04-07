if (document.readyState != "complete"){}  // The equivalent of using "pass" in "Python".
 
AgregarEventoAEnlaces();  // Agregamos un evento "onclick" al enlace, para poder activar una función cada que hagamos click en cualquiera de ellos.
// De esta forma, cada que demos click sobre "Añadir a la Canasta" recuperaremos el Precio y Nombre de dicho producto guardado en Almacenamiento Local.

ItemsEnCanasta();  // Siempre que se cargue la página del "Menú", se cargarán los items (si hay), cargados con aterioridad en casta.

VerificandoCanasta();  // Para verificar que productos ya se encuentran en la canasta y deshabilitarlos de nueva cuenta, en caso de refrescar la
// página o irse a otra pestaña y después regresar al menú.

function ItemsEnCanasta(){  // En caso de que ya existan items en la canasta, recuperaremos la cantidad total para mostrarlos. De esta forma si
    // el usuario cambia de pestaña o recarga la página del Ménu, se seguirán mostrando la cantidad total de items en canasta.

    // var Cantidad_Productos = localStorage.getItem("Cantidad_Item");
    // var Datos_Cliente = localStorage.getItem("Cliente_id");

    // if (Cantidad_Productos && Datos_Cliente){
    //     document.getElementById("cantidad_canasta").innerText = Cantidad_Productos - 1;
    // } else if (Cantidad_Productos){
    //     document.getElementById("cantidad_canasta").innerText = Cantidad_Productos;
    // }

    var Datos_Cliente = localStorage.getItem("Cliente_id");

    if (Datos_Cliente){
        document.getElementById("cantidad_canasta").innerText = localStorage.length-1;
    } else {
        document.getElementById("cantidad_canasta").innerText = localStorage.length;
    }

}


function AgregarEventoAEnlaces(){   
    var enlaces_en_texto = document.querySelectorAll(".text-content a");  // document.querySelectorAll("html tag con dicha clase > html tag").
    var enlaces_en_imagen = document.querySelectorAll(".food-item a");

    for(var i = 0; i < enlaces_en_texto.length; i++){
        enlaces_en_texto[i].addEventListener("click", () => {
            console.log("AÑADIDO :)");
            agregar_items_canasta(event);
            cambiar_color_canasta(event);
        });
    }
};


function cambiar_color_canasta(event){
    setTimeout(() => {if (event.type == "click") {
        document.getElementById("carrito_contenedor").setAttribute("style", "background-color: #ffa600;")
    }}, 150);
    document.getElementById("carrito_contenedor").setAttribute("style", "background-color: rgb(214, 0, 14);")
};


function agregar_items_canasta(event){

    // var Cantidad_Producto = localStorage.getItem("Cantidad_Item");  // Será NaN si es la primera vez que ingresamos el artículo al carrito,
    // // dado que no obtendremos nada.
    //

    // Cantidad_Producto = parseInt(Cantidad_Producto)  // Convertimos a Entero.
    // if (Cantidad_Producto){  // En caso de que volvamos a agregar por segunda vez dicho artículo. Por lo tanto, dado que esta variable ya tiene
    //     // contenido, el booleano equivalente sería "true".
    //     localStorage.setItem("Cantidad_Item", Cantidad_Producto + 1);
    //     document.getElementById("cantidad_canasta").innerText = Cantidad_Producto + 1;
    // } else{
    //     localStorage.setItem("Cantidad_Item", 1);
    //     document.getElementById("cantidad_canasta").innerText = 1;
    // }

    ObteniendoYGuardandoDatosProductos(event);  // Para guardar el Precio y Nombre del producto correspondiente en Almacenamiento Local.

    var Datos_Cliente = localStorage.getItem("Cliente_id");
    var Pagina_Previa = localStorage.getItem("Bandera_Regreso");

    if (Datos_Cliente && Pagina_Previa) {
        document.getElementById("cantidad_canasta").innerText = localStorage.length - 2;
    } else if (Datos_Cliente || Pagina_Previa){
        document.getElementById("cantidad_canasta").innerText = localStorage.length - 1;
    } else {
        document.getElementById("cantidad_canasta").innerText = localStorage.length;
    }
};


function ObteniendoYGuardandoDatosProductos(event){  // Recueperamos el Precio y Nombre de cada producto guardado en Almacenamiento Local.
    var enlace = event.target  // Nos situamos en el enlace "Añadir a la Canasta".
    if (enlace.innerText != "Ya en Canasta :)"){
        var contenedor_producto = enlace.parentElement.parentElement  // Obtenemos el Contenedor abuelo de dicho enlace y acotamos nuestra selección a esté mismo.
        var precio = parseFloat(contenedor_producto.querySelector('.price').innerText.replace('$',''))
        var nombre_producto = contenedor_producto.querySelector(".text-content h4").innerText
        
        console.log("PRECIO:", precio);
        console.log("PRODUCTO:", nombre_producto);

        const obj_alimento = {
            "id": nombre_producto,
            "precio": precio,
            "CantidadEnCanasta": 1,
        }
        localStorage.setItem(nombre_producto, JSON.stringify(obj_alimento));  // Guardamos el objecto creado en Almacenamiento Local.
        
        // Para evitar que el usuario pueda agregar más de 1 vez el mismo producto a la canasta:
        event.target.innerText = "Ya en Canasta :)"  // Para notificar al usuario que el producto ya esta en la canasta.
        event.target.style = "pointer-events: none;"  // Para deshabilitar el link que permite agregar el producto a la canasta.
    }
}


function VerificandoCanasta(){  // Siempre que refresquemos la pág o cambiemos de sitio para despúes regresar al menú, inhabilitaremos todos
    // aquellos elementos que ya se encuentran en la canasta.
    let etiquetas_h4 = document.querySelectorAll(".text-content h4");  // document.querySelectorAll("html tag con dicha clase > html tag hijo").
    let nombre_items = [];
    for (let i = 0; i < etiquetas_h4.length; i++){
        nombre_items.push(etiquetas_h4[i].innerText)
    }
    for (let i = 0; i < localStorage.length; i++){
        let elemento_en_canasta = JSON.parse(localStorage.getItem(localStorage.key(i)));
        if (nombre_items.includes(elemento_en_canasta.id)){
            // Usamos "xpath" para localizar los elementos que ya han sido agregados a la página:
            let xpath = `//div[@class='text-content']/h4[text()='${elemento_en_canasta.id}']`
            let ElementoHallado = document.evaluate(xpath, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            ElementoHallado.parentElement.getElementsByTagName('a')[0].innerText = "Ya en Canasta :)";
            ElementoHallado.parentElement.getElementsByTagName('a')[0].style = "pointer-events: none;";
        }
    }
}

















//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// if (document.readyState !== "complete"){}  // The equivalent of using "pass" in "Python".
 
// AgregarEventoAEnlaces();  // Agregamos un evento "onclick" al enlace, para poder activar una función cada que hagamos click en cualquiera de ellos.
// // De esta forma, cada que demos click sobre "Añadir a la Canasta" recuperaremos el Precio y Nombre de dicho producto guardado en Almacenamiento Local.

// ItemsEnCanasta();  // Siempre que se cargue la página del "Menú", se cargarán los items (si hay), cargados con aterioridad en casta.

// function ItemsEnCanasta(){  // En caso de que ya existan items en la canasta, recuperaremos la cantidad total para mostrarlos. De esta forma si
//     // el usuario cambia de pestaña o recarga la página del Ménu, se seguirán mostrando la cantidad total de items en canasta.

//     var Cantidad_Productos = localStorage.getItem("Cantidad_Item");

//     if(Cantidad_Productos){
//         document.getElementById("cantidad_canasta").innerText = Cantidad_Productos;
//     }
// }


// function AgregarEventoAEnlaces(){   
//     var enlaces = document.querySelectorAll(".text-content a");  // document.querySelectorAll("html tag con dicha clase > html tag hijo").
//     for(var i = 0; i < enlaces.length; i++){
//         enlaces[i].addEventListener("click", () => {
//             console.log("AÑADIDO :)");
//             agregar_items_canasta(event);
//             costo_total();  // De esta forma, cada que hagamos click sobre cualquier enlace, el costo total del carrito se actualizará.
//             cambiar_color_canasta(event);
//         });
//     }
// }

// function cambiar_color_canasta(event){
//     setTimeout(() => {if (event.type == "click") {
//         document.getElementById("carrito_contenedor").setAttribute("style", "background-color: #ffa600;")
//     }}, 150);
//     document.getElementById("carrito_contenedor").setAttribute("style", "background-color: rgb(214, 0, 14);")
// }

// function agregar_items_canasta(event){
//     var Cantidad_Producto = localStorage.getItem("Cantidad_Item");  // Será NaN si es la primera vez que ingresamos el artículo al carrito,
//     // dado que no obtendremos nada.

//     Cantidad_Producto = parseInt(Cantidad_Producto)  // Convertimos a Entero.
//     if (Cantidad_Producto){  // En caso de que volvamos a agregar por segunda vez dicho artículo. Por lo tanto, dado que esta variable ya tiene
//         // contenido, el booleano equivalente sería "true".
//         localStorage.setItem("Cantidad_Item", Cantidad_Producto + 1);
//         document.getElementById("cantidad_canasta").innerText = Cantidad_Producto + 1;
//     } else{
//         localStorage.setItem("Cantidad_Item", 1);
//         document.getElementById("cantidad_canasta").innerText = 1;
//     }

//     ObteniendoYGuardandoDatosProductos(event);  // Para guardar el Precio y Nombre del producto correspondiente en Almacenamiento Local.
// };


// function ObteniendoYGuardandoDatosProductos(event){  // Recueperamos el Precio y Nombre de cada producto guardado en Almacenamiento Local.
//     var enlace = event.target  // Nos situamos en el enlace "Añadir a la Canasta".
//     var contenedor_producto = enlace.parentElement.parentElement  // Obtenemos el Contenedor abuelo de dicho enlace y acotamos nuestra selección a esté mismo.
//     var precio = parseFloat(contenedor_producto.querySelector('.price').innerText.replace('$',''))
//     var nombre_producto = contenedor_producto.querySelector(".text-content h4").innerText
//     console.log("PRECIO:", precio);
//     console.log("PRODUCTO:", nombre_producto);

//     var canasta_item = JSON.parse(localStorage.getItem(nombre_producto))  // De esta forma convertimos de un Objecto JSON a JS.
//     if (canasta_item != null){
//         canasta_item.CantidadEnCanasta += 1;  // Aumentamos el número de veces que aparece este producto en la canasta.
//         localStorage.setItem(nombre_producto, JSON.stringify(canasta_item));  // Sobrescribimos el item con la nueva cantidad y lo guardamos en AL.
//     } else {  // Si el producto no aparece, lo creamos.
//         const obj_alimento = {
//             "id": nombre_producto,
//             "precio": precio,
//             "CantidadEnCanasta": 1,  // Para incrementar la cantidad del producto en la canasta.
//         }
    
//         localStorage.setItem(nombre_producto, JSON.stringify(obj_alimento));
//     }
// }


// function costo_total(){  // Para calcular el costo total de la canasta.
//     var total_canasta = 0
//     for (var i = 0; i < localStorage.length; i++){
//         var item_diccionario = JSON.parse(localStorage.getItem(localStorage.key(i)))
//         if (item_diccionario.id != undefined){
//             total_canasta += (item_diccionario.precio * item_diccionario.CantidadEnCanasta)
//         }
//     }
//     console.log("TOTAL A PAGAR:", total_canasta)
// }
