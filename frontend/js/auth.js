/*
  auth.js
  ------------------------------------------------------------
  Handles: showing the right navbar links, and the
  login / register form submissions.
  ------------------------------------------------------------
*/

// Runs on every page load to update the navbar
async function loadNavbar() {
    const navRight = document.getElementById("nav-right");
    if (!navRight) return;

    try {
        const me = await apiCall("/api/me");
        if (me.logged_in) {
            navRight.innerHTML = `
                <span>Hi, ${me.name}</span>
                ${me.is_admin ? '<a href="admin.html">Admin</a>' : ''}
                <a href="orders.html">My Orders</a>
                <a href="cart.html">Cart <span class="cart-badge" id="cart-count">0</span></a>
                <a href="#" id="logout-link">Logout</a>
            `;
            document.getElementById("logout-link").addEventListener("click", async (e) => {
                e.preventDefault();
                await apiCall("/api/logout", "POST");
                window.location.href = "index.html";
            });
        } else {
            navRight.innerHTML = `
                <a href="cart.html">Cart <span class="cart-badge" id="cart-count">0</span></a>
                <a href="login.html">Login</a>
                <a href="register.html">Register</a>
            `;
        }
        updateCartBadge();
    } catch (err) {
        console.error(err);
    }
}

// LOGIN FORM
function setupLoginForm() {
    const form = document.getElementById("login-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const errorBox = document.getElementById("form-error");
        errorBox.textContent = "";

        try {
            await apiCall("/api/login", "POST", {
                email: form.email.value,
                password: form.password.value,
            });
            window.location.href = "index.html";
        } catch (err) {
            errorBox.textContent = err.message;
        }
    });
}

// REGISTER FORM
function setupRegisterForm() {
    const form = document.getElementById("register-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const errorBox = document.getElementById("form-error");
        errorBox.textContent = "";

        try {
            await apiCall("/api/register", "POST", {
                name: form.name.value,
                email: form.email.value,
                password: form.password.value,
                address: form.address.value,
                phone: form.phone.value,
            });
            window.location.href = "index.html";
        } catch (err) {
            errorBox.textContent = err.message;
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    loadNavbar();
    setupLoginForm();
    setupRegisterForm();
});
