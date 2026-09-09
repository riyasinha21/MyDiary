console.log("login.js loaded");


document.addEventListener("DOMContentLoaded", function () {


    const form = document.getElementById("loginForm");

    const emailInput = document.getElementById("email");

    const passwordInput = document.getElementById("password");

    const emailError = document.getElementById("emailError");

    const passwordError = document.getElementById("passwordError");

    const loginError = document.getElementById("loginError");

    const togglePassword = document.getElementById("togglePassword");

    const passwordIcon = document.getElementById("passwordIcon");

/* ============================= PASSWORD SHOW / HIDE ========================================== */

    togglePassword.addEventListener("click", function () {

        if (passwordInput.type === "password") {

            passwordInput.type = "text";

            passwordIcon.classList.remove("bi-eye");
            passwordIcon.classList.add("bi-eye-slash");

            togglePassword.setAttribute( "aria-label", "Hide password" );

        } else {

            passwordInput.type = "password";

            passwordIcon.classList.remove("bi-eye-slash");
            passwordIcon.classList.add("bi-eye");

            togglePassword.setAttribute( "aria-label", "Show password" );

        }

    });


    // Clear email error when user starts typing
    emailInput.addEventListener("input", function () {

        if (emailError){
            emailError.textContent = "";
        }
        
        if (loginError){
            loginError.textContent = "";
        }
    });

    // Clear password error when user starts typing
    passwordInput.addEventListener("input", function () {

        if (passwordError){
            passwordError.textContent = "";
        }

        if (loginError){
            loginError.textContent = "";
        }

    });


});