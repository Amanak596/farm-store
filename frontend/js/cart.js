/*
  cart.js
  ------------------------------------------------------------
  The cart is kept in the browser (localStorage) until the
  customer checks out. At checkout, cart.js sends the cart
  items to the backend, which creates the real order.
  ------------------------------------------------------------
*/

function getCart() {
    return JSON.parse(localStorage.getItem("cart") || "[]");
}

function saveCart(cart) {
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartBadge();
}

function addToCart(product, quantity) {
    const cart = getCart();
    const existing = cart.find((item) => item.product_id === product.id);

    if (existing) {
        existing.quantity += quantity;
    } else {
        cart.push({
            product_id: product.id,
            name: product.name,
            price: parseFloat(product.price),
            image_url: product.image_url,
            quantity: quantity,
        });
    }
    saveCart(cart);
}

function removeFromCart(productId) {
    const cart = getCart().filter((item) => item.product_id !== productId);
    saveCart(cart);
}

function updateCartItemQuantity(productId, quantity) {
    const cart = getCart();
    const item = cart.find((i) => i.product_id === productId);
    if (item) {
        item.quantity = Math.max(1, quantity);
        saveCart(cart);
    }
}

function clearCart() {
    localStorage.removeItem("cart");
    updateCartBadge();
}

function getCartTotal() {
    return getCart().reduce((sum, item) => sum + item.price * item.quantity, 0);
}

function updateCartBadge() {
    const badge = document.getElementById("cart-count");
    if (badge) badge.textContent = getCart().length;
}
