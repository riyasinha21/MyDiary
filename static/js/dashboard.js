console.log("dashboard.js loaded");

document.addEventListener("DOMContentLoaded", function () {

    const accessToken = localStorage.getItem("access_token");

    if (!accessToken) {

        alert("Please login first.");

        window.location.href = "/api/user/login-page/";

        return;
    }

    document.getElementById("logoutBtn")
        .addEventListener("click", function () {

            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");

            alert("Logged out successfully.");

            window.location.href = "/api/user/login-page/";

        });

});