document.addEventListener("DOMContentLoaded", function () {

    /* ==========================================
       RESTORE COMMUNITY SCROLL POSITION
    ========================================== */

    const savedScrollPosition =
        sessionStorage.getItem("communityScrollPosition");

    if (savedScrollPosition !== null) {

        setTimeout(function () {

            window.scrollTo(
                0,
                parseInt(savedScrollPosition, 10)
            );

            sessionStorage.removeItem(
                "communityScrollPosition"
            );

        }, 50);
    }


    /* ==========================================
       SAVE COMMUNITY SCROLL POSITION
    ========================================== */

    const friendForms =
        document.querySelectorAll(".friend-action-form");

    friendForms.forEach(function (form) {

        form.addEventListener("submit", function () {

            sessionStorage.setItem(
                "communityScrollPosition",
                window.scrollY
            );

        });

    });


    /* ==========================================
       COMMENT TOGGLE
    ========================================== */

    const commentButtons =
        document.querySelectorAll(".comment-toggle-btn");

    commentButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const commentsId =
                button.getAttribute("data-comments");

            const commentsSection =
                document.getElementById(commentsId);

            if (!commentsSection) {
                return;
            }

            commentsSection.classList.toggle("active");

        });

    });

});