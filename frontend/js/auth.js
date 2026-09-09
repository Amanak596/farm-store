async function updateNavbar() {

const navRight =
    document.getElementById("nav-right");


if (!navRight) {
    return;
}


try {

    const me =
        await apiCall("/api/me");


    if (me.logged_in) {

        navRight.innerHTML = `

            <a href="orders.html">
                📦 Orders
            </a>

            <span class="nav-user">
                👋 ${me.name || "User"}
            </span>

            <button
                class="logout-btn"
                onclick="logoutUser()"
            >
                Logout
            </button>

        `;

    } else {

        navRight.innerHTML = `

            <a href="login.html">
                Login
            </a>

            <a
                href="register.html"
                class="nav-register"
            >
                Register
            </a>

        `;

    }


} catch (error) {

    navRight.innerHTML = `

        <a href="login.html">
            Login
        </a>

    `;

}


}

async function logoutUser() {

try {

    await apiCall(
        "/api/logout",
        "POST"
    );

    window.location.href =
        "index.html";

} catch (error) {

    console.error(
        "Logout failed:",
        error
    );

}


}

document.addEventListener(
"DOMContentLoaded",
updateNavbar
);
