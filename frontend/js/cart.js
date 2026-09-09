const CART_KEY = "farmstore_cart";

function getCart() {

try {

    const saved =
        localStorage.getItem(CART_KEY);

    return saved
        ? JSON.parse(saved)
        : [];

} catch (error) {

    console.error(
        "Could not read cart:",
        error
    );

    return [];

}


}

function saveCart(cart) {

localStorage.setItem(
    CART_KEY,
    JSON.stringify(cart)
);

updateCartCount();


}

function addToCart(product, quantity = 1) {

const cart = getCart();

const qty =
    parseInt(quantity) || 1;


const existing =
    cart.find(
        item =>
            Number(item.product_id) ===
            Number(product.id)
    );


if (existing) {

    existing.quantity += qty;

} else {

    cart.push({

        product_id:
            Number(product.id),

        name:
            product.name,

        price:
            Number(product.price),

        quantity:
            qty,

        image_url:
            product.image_url ||
            "images/placeholder.jpg"

    });

}


saveCart(cart);


}

function updateCartItemQuantity(
productId,
quantity
) {

const cart = getCart();

const item =
    cart.find(
        item =>
            Number(item.product_id) ===
            Number(productId)
    );


if (!item) {
    return;
}


item.quantity =
    parseInt(quantity) || 1;


if (item.quantity < 1) {

    removeFromCart(productId);

    return;

}


saveCart(cart);


}

function removeFromCart(productId) {

const cart =
    getCart().filter(
        item =>
            Number(item.product_id) !==
            Number(productId)
    );


saveCart(cart);


}

function clearCart() {

localStorage.removeItem(
    CART_KEY
);

updateCartCount();


}

function getCartTotal() {

return getCart().reduce(
    (total, item) => {

        return total +
            (
                Number(item.price) *
                Number(item.quantity)
            );

    },
    0
);


}

function updateCartCount() {

const count =
    getCart().reduce(
        (total, item) =>
            total +
            Number(item.quantity),
        0
    );


document
    .querySelectorAll(
        "#cart-count"
    )
    .forEach(element => {

        element.textContent =
            count;

    });


}

document.addEventListener(
"DOMContentLoaded",
updateCartCount
);
