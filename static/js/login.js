console.log("login.js loaded");


document.addEventListener("DOMContentLoaded", function () {


    const form = document.getElementById("loginForm");

    const emailInput = document.getElementById("email");

    const passwordInput = document.getElementById("password");

    const emailError = document.getElementById("emailError");

    const passwordError = document.getElementById("passwordError");

    const loginError = document.getElementById("loginError");

    const successPopup = document.getElementById("successPopup");

    // Clear email error when user starts typing
    emailInput.addEventListener("input", function () {

        emailError.textContent = "";

        loginError.textContent = "";

    });


    // Clear password error when user starts typing
    passwordInput.addEventListener("input", function () {

        passwordError.textContent = "";

        loginError.textContent = "";

    });


    form.addEventListener("submit", async function (event) {


        // Prevent normal form submission and page reload
        event.preventDefault();


        console.log("Login form submitted");


        // Clear previous errors
        emailError.textContent = "";

        passwordError.textContent = "";

        loginError.textContent = "";


        const data = {

            email: document.getElementById("email").value,

            password: document.getElementById("password").value

        };


        console.log(data);


        try {


            const response = await fetch("/api/user/login/", {


                method: "POST",


                headers: {

                    "Content-Type": "application/json"

                },


                body: JSON.stringify(data)


            });


            const result = await response.json();


            console.log("Status:", response.status);

            console.log("Response:", result);


            if (response.ok) {

                // Show success popup
                successPopup.style.display = "flex";
                

                // Save JWT tokens

                localStorage.setItem(
                    "access_token",
                    result.token.access
                );


                localStorage.setItem(
                    "refresh_token",
                    result.token.refresh
                );


                
                 // Redirect after 1.5 seconds
                setTimeout(function () {
                    window.location.href = "/api/user/home-page/";
                }, 1500);

            } else {


                // Email validation error
                if (result.email) {

                    emailError.textContent = result.email[0];

                }


                // Password validation error
                if (result.password) {

                    passwordError.textContent = result.password[0];

                }


                // General login error
                if (result.message) {

                    loginError.textContent = result.message;

                }


            }


        } catch(error) {


            console.error(error);

            loginError.textContent = "Something went wrong. Please try again.";


        }


    });


});