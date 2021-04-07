if (document.readyState != "complete"){}  // The equivalent of using "pass" in "Python".

$(document).ready(function() {
    // DESHABILITAMOES LA RUEDA DEL MOUSE, CON LA FINALIDAD DE EVITAR UN BUG QUE NO DESENCADENA LAS FUNCIONES ATADAS AL EVENTO "wheel".
    $('input[type=number]').on('wheel',function(e){ $(this).blur(); }); 
});

ImprimiendoProductos();
updateCartTotal();

function ImprimiendoProductos(){
    for(let i = 0; i < localStorage.length; i++){
        let producto_en_canasta = JSON.parse(localStorage.getItem(localStorage.key(i)));
        if (producto_en_canasta.id != undefined){
            //console.log("PRODUCTO: ", producto_en_canasta);

            var cartRow = document.createElement('div')
            cartRow.classList.add('cart-row')
            var cartItems = document.getElementsByClassName('cart-items')[0]

            var cantidad = producto_en_canasta.CantidadEnCanasta  // De entrada, canasta debe ser == 1 por default al agregar al menú.

            var cartRowContents = `
                <div class="cart-item cart-column">
                    <span class="cart-item-title">${producto_en_canasta.id}</span>
                </div>
                <span class="cart-price cart-column">${producto_en_canasta.precio}</span>
                <div class="cart-quantity cart-column">
                    <input class="cart-quantity-input" type="number" min="1" value="${cantidad}"></input>
                    <button class="btn btn-danger" type="button">Remover</button>
                </div>`
            cartRow.innerHTML = cartRowContents
            cartItems.append(cartRow)
            cartRow.getElementsByClassName('btn-danger')[0].addEventListener("click", () => {RemoverItems(event), GuardarDatosCanasta()});
            cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener("click", GuardarDatosCanasta);
            // Agregamos un tipo de evento "keyup" extra en las flechitas de cantidad, para que en caso de que el usuario use las 
            // flechas del teclado para agregar o quitar la cantidad del alimento, los datos se sigan guardando
            // y actualizando: 
            cartRow.getElementsByClassName('cart-quantity-input')[0].addEventListener("keyup", () => {GuardarDatosCanasta(),  
                EvitarValoresMenoresAUno(event)});

            // NOTA: AL AGREGAR UN EVENTO CON "addEventListener()", SI DESEAMOS PASAR UNA SOLA FUNCIÓN QUE NO REQUIERA PARÁMETROS, 
            // BASTA CON DECLARLA SIN LOS PARÉNTISIS. POR OTRO LADO, SI DESEAMOS PASAR MÁS DE UNA FUNCIÓN, DEBEMOS HACER USO DE UNA FUNCIÓN
            // ANÓNIMA: 
            //                  () => {Función_1(event), Función_2(), Función_3(param_1, param_2, ..., para_N)}
            // ESTO SE APRECIA, EN EL PRIMER EVENTO AÑADIDO "click".
        }
    }
}


function RemoverItems(event) {
    var buttonClicked = event.target; // Buscamos los elementos a partir del botón en donde hicimos click.
    
    // Borramos el item en conjunto con su información del árbol html:
    buttonClicked.parentElement.parentElement.remove();
    
    // Borramos del "Almacenamiento Local" al Item deseado:
    let nombre_producto = buttonClicked.parentElement.parentElement.getElementsByClassName("cart-item-title")[0].innerText;
    localStorage.removeItem(nombre_producto);

    // Verificamos constantemente que la canasta no quede vacía. De ser así, deshabilitamos el botón de "ORDENAR":
    let elementos_en_carrito = document.getElementsByClassName("cart-items")[0].children // Bandera para saber si la clase "car-items"
    // contiene elementos del carrito desplegados.
    if (elementos_en_carrito.length == 0){  // En caso de que no haya elementos desplegados (lo que significa que la canasta esta vacía),
        // el botón de "ORDENAR" se deshabilitará.
        document.getElementsByClassName('btn-purchase')[0].disabled = true;
    }

    // Actualizamos el carrito para reflejar los cambios:
    updateCartTotal();

    // Reducimos la Cantidad de Items totales en la canasta cada que se de click en Remove. Por otro lado, de no haber elementos,
    // limpiamos la canasta:
    // if (localStorage.length <= 1){  // Si solo resta un elemento, después de borrar todos los contenidos en la canasta, significa que solo queda
    //     // el elemento bandera "Cantidad_Item", por lo que la canasta esta vacía y debemos vaciar el almacenamiento local.
    //     localStorage.clear();
    // } else{
    //     localStorage.setItem("Cantidad_Item", localStorage.length-1)  // "-1" Dado que "Cantidad_Item" JS lo cuenta también como elemento.
    // }
}


async function EvitarValoresMenoresAUno(event) {
    var input = event.target
    // console.log("VAR: ",input.value)
    // console.log("IS NAN: ", isNaN(input.value))
    // console.log("IS EMPTY STRING: ", input.value == false)
    if (input.value == false) {
        console.log("Taking a break");
        await new Promise(r => setTimeout(r, 3500));  // Para dormir 3.5s.
        console.log("Awaking");
    } 
    
    if (isNaN(input.value) || input.value <= 0) {
        input.value = 1
    }

    updateCartTotal()
}


function GuardarDatosCanasta(){
    var cartItemContainer = document.getElementsByClassName('cart-items')[0];
    var cartRows = cartItemContainer.getElementsByClassName('cart-row');
    let fila = 0
    for(let i = 0; i < localStorage.length; i++){
        var canasta_item = JSON.parse(localStorage.getItem(localStorage.key(i)));  // De esta forma convertimos de un Objecto JSON a JS.
        if(canasta_item.id != undefined){
            var cartRow = cartRows[fila];
            // console.log("ELEMENTO i:", i)
            // console.log("CART ROW:", cartRow)
            // console.log("QUANTITY:", cartRow.getElementsByClassName('cart-quantity-input')[0].value, '\n')
            canasta_item.CantidadEnCanasta = cartRow.getElementsByClassName('cart-quantity-input')[0].value;
            localStorage.setItem(canasta_item.id, JSON.stringify(canasta_item));  // Sobrescribimos el item con la nueva cantidad y lo guardamos en AL.
            fila ++;
        }
    }
    updateCartTotal()
}


function updateCartTotal() {
    var cartItemContainer = document.getElementsByClassName('cart-items')[0]
    var cartRows = cartItemContainer.getElementsByClassName('cart-row')
    var total = 0
    for (var i = 0; i < cartRows.length; i++) {
        var cartRow = cartRows[i]
        var priceElement = cartRow.getElementsByClassName('cart-price')[0]
        var quantityElement = cartRow.getElementsByClassName('cart-quantity-input')[0]
        var price = parseFloat(priceElement.innerText.replace('$', ''))
        var quantity = quantityElement.value
        total = total + (price * quantity)
    }
    total = Math.round(total * 100) / 100
    document.getElementsByClassName('cart-total-price')[0].innerText = '$' + total
}