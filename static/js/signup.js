console.log("signup.js loaded");

document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // ELEMENTS
    // ==========================================

    const passwordInput =
        document.getElementById("password");

    const togglePassword =
        document.getElementById("togglePassword");

    const confirmPasswordInput =
        document.getElementById("confirm_password");

    const toggleConfirmPassword =
        document.getElementById("toggleConfirmPassword");

    const phoneInput =
        document.getElementById("phone_number");

    const countryDropdownBtn =
        document.getElementById("countryDropdownBtn");

    const countryDropdownList =
        document.getElementById("countryDropdownList");

    const selectedCountry =
        document.getElementById("selectedCountry");

    const countryCodeInput =
        document.getElementById("country_code");


    // ==========================================
    // PASSWORD VISIBILITY
    // ==========================================

    togglePassword.addEventListener("click", function () {

        const icon =
            togglePassword.querySelector("i");

        if (passwordInput.type === "password") {

            passwordInput.type = "text";

            icon.classList.remove("bi-eye");
            icon.classList.add("bi-eye-slash");

        } else {

            passwordInput.type = "password";

            icon.classList.remove("bi-eye-slash");
            icon.classList.add("bi-eye");

        }

    });


    // ==========================================
    // CONFIRM PASSWORD VISIBILITY
    // ==========================================

    toggleConfirmPassword.addEventListener("click", function () {

        const icon =
            toggleConfirmPassword.querySelector("i");

        if (confirmPasswordInput.type === "password") {

            confirmPasswordInput.type = "text";

            icon.classList.remove("bi-eye");
            icon.classList.add("bi-eye-slash");

        } else {

            confirmPasswordInput.type = "password";

            icon.classList.remove("bi-eye-slash");
            icon.classList.add("bi-eye");

        }

    });


    // ==========================================
    // COUNTRY DROPDOWN
    // ==========================================

    countryDropdownBtn.addEventListener("click", function (event) {

        event.stopPropagation();

        countryDropdownList.classList.toggle("show");

    });

// ==========================================
// SELECT COUNTRY
// ==========================================

function countryFlag(countryCode) {

    return countryCode
        .toUpperCase()
        .split("")
        .map(function (char) {

            return String.fromCodePoint(
                char.charCodeAt(0) + 127397
            );

        })
        .join("");
}


const countryOptions =
    document.querySelectorAll(".country-option");


countryOptions.forEach(function (option) {

    const country =
        option.dataset.country;

    const code =
        option.dataset.code;

    const flag =
        countryFlag(country);


    // Show flag + calling code in dropdown

    const flagElement =
        option.querySelector(".country-flag");

    if (flagElement) {

        flagElement.textContent =
            flag;

    }


    option.addEventListener("click", function () {

        // Show selected flag + calling code

        selectedCountry.textContent =
            flag + " " + code;


        // Store ONLY calling code

        countryCodeInput.value =
            code;


        // Clear phone number

        phoneInput.value = "";


        // Close dropdown

        countryDropdownList.classList.remove("show");

    });

});


    // ==========================================
    // CLOSE DROPDOWN OUTSIDE CLICK
    // ==========================================

    document.addEventListener("click", function (event) {

        if (!event.target.closest(".country-dropdown")) {

            countryDropdownList.classList.remove("show");

        }

    });

});