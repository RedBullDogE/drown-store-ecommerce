let buttonMinusArray = document.getElementsByClassName("button-minus")
let quantityField = document.getElementsByClassName("quantity-value")
let buttonPlusArray = document.getElementsByClassName("button-plus")

Array.from(buttonPlusArray).forEach((btn, index) => {
    btn.onclick = async () => {
        console.log("kek", index);
        let url = "{% url 'core:add-to-cart-ajax' order_item.item.slug %}";
        let response = await fetch(url);

        if (response.ok) {
            quantityField[index].innerHTML = +quantityField[index].innerHTML + 1
        } else {
            alert("HTTP Error: " + response.status);
        }
    }
});


