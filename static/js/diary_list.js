document.addEventListener("DOMContentLoaded", function () {

    /* =========================
       POST MORE MENU
    ========================= */

    const moreButtons =
        document.querySelectorAll(".post-more-btn");


    moreButtons.forEach(function (button) {

        button.addEventListener("click", function (event) {

            event.stopPropagation();

            const postMenu =
                button.closest(".post-menu");


            document
                .querySelectorAll(".post-menu.active")
                .forEach(function (menu) {

                    if (menu !== postMenu) {

                        menu.classList.remove("active");

                    }

                });


            postMenu.classList.toggle("active");

        });

    });


    document.addEventListener("click", function () {

        document
            .querySelectorAll(".post-menu.active")
            .forEach(function (menu) {

                menu.classList.remove("active");

            });

    });


    /* =========================
       COMMENT TOGGLE
    ========================= */

    const commentButtons =
        document.querySelectorAll(".comment-toggle-btn");


    commentButtons.forEach(function (button) {

        button.addEventListener("click", function () {

            const postCard =
                button.closest(".post-card" ,".community-diary-card");


            const commentForm =
                postCard.querySelector(".comment-form");


            const commentsSection =
                postCard.querySelector(".comments-section");


            if (!commentForm || !commentsSection) {
                console.log("Comment elements not found");
                return;
            }


            commentForm.classList.toggle("active");

            commentsSection.classList.toggle("active");


            if (commentForm.classList.contains("active")) {

                const input =
                    commentForm.querySelector("input");

                input.focus();

            }

        });

    });

});

document.addEventListener("DOMContentLoaded", function () {

    // Save scroll position before like/comment/bookmark form submits
    const actionForms = document.querySelectorAll(
        '.post-footer form, .comment-form'
    );

    actionForms.forEach(function (form) {

        form.addEventListener("submit", function () {

            sessionStorage.setItem(
                "scrollPosition",
                window.scrollY
            );

        });

    });


    // Restore scroll position after page reload
    const scrollPosition = sessionStorage.getItem(
        "scrollPosition"
    );

    if (scrollPosition !== null) {

        window.scrollTo(
            0,
            parseInt(scrollPosition)
        );

        sessionStorage.removeItem(
            "scrollPosition"
        );

    }

});