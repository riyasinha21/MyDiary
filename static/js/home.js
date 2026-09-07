console.log("home.js loaded");


document.addEventListener("DOMContentLoaded", function () {

    /*
    ==========================================
    ELEMENT REFERENCES
    ==========================================
    */

    const diaryModal =
        document.getElementById("diaryModal");

    const openDiaryButton =
        document.getElementById("openDiaryModal");

    const openDiaryFromHome =
        document.getElementById("openDiaryFromHome");

    const closeDiaryButton =
        document.getElementById("closeDiaryModal");

    const diaryContent =
        document.getElementById("diaryContent");

    const wordCount =
        document.getElementById("wordCount");

    const contentError =
        document.getElementById("contentError");

    const emojiBtn =
        document.getElementById("emojiBtn");

    const visibilityInput =
        document.getElementById("diaryVisibility");

    const visibilityIcon =
        document.getElementById("visibilityIcon");

    const diaryDate =
        document.getElementById("diaryDate");


    /*
    ==========================================
    OPEN MODAL
    ==========================================
    */

    function openDiaryModal() {

        if (!diaryModal) {
            return;
        }

        diaryModal.classList.add("active");

        document.body.style.overflow = "hidden";

    }


    /*
    ==========================================
    CLOSE MODAL
    ==========================================
    */

    function closeDiaryModal() {

        if (!diaryModal) {
            return;
        }

        diaryModal.classList.remove("active");

        document.body.style.overflow = "";

    }


    /*
    ==========================================
    NAVBAR WRITE BUTTON
    ==========================================
    */

    if (openDiaryButton) {

        openDiaryButton.addEventListener(
            "click",
            openDiaryModal
        );

    }


    /*
    ==========================================
    WRITE TODAY'S DIARY BUTTON
    ==========================================
    */

    if (openDiaryFromHome) {

        openDiaryFromHome.addEventListener(
            "click",
            openDiaryModal
        );

    }


    /*
    ==========================================
    CLOSE BUTTON
    ==========================================
    */

    if (closeDiaryButton) {

        closeDiaryButton.addEventListener(
            "click",
            closeDiaryModal
        );

    }


    /*
    ==========================================
    CLICK OUTSIDE MODAL
    ==========================================
    */

    if (diaryModal) {

        diaryModal.addEventListener(
            "click",
            function (event) {

                if (event.target === diaryModal) {

                    closeDiaryModal();

                }

            }
        );

    }


    /*
    ==========================================
    WORD COUNT
    ==========================================
    */

    if (diaryContent && wordCount) {

        diaryContent.addEventListener(
            "input",
            function () {

                const text =
                    diaryContent.value.trim();


                const words =
                    text
                        ? text.split(/\s+/).filter(Boolean).length
                        : 0;


                wordCount.textContent =
                    words;


                /*
                ==================================
                CLEAR CONTENT ERROR
                ==================================
                */

                if (words >= 10) {

                    if (contentError) {

                        contentError.textContent = "";

                    }

                    diaryContent.classList.remove(
                        "input-error"
                    );

                }

            }
        );

    }


    /*
    ==========================================
    EMOJI PICKER
    ==========================================
    */

    if (
        emojiBtn &&
        diaryContent &&
        typeof EmojiMart !== "undefined"
    ) {

        const emojiWrapper =
            document.createElement("div");


        emojiWrapper.className =
            "emoji-picker-wrapper";


        emojiWrapper.style.display =
            "none";


        /*
        ======================================
        CREATE EMOJI PICKER
        ======================================
        */

        const picker =
            new EmojiMart.Picker({

                onEmojiSelect:
                    function (emoji) {

                        insertEmoji(
                            emoji.native
                        );

                        emojiWrapper.style.display =
                            "none";

                    },

                theme: "light",

                set: "native",

                previewPosition: "bottom",

                searchPosition: "top"

            });


        emojiWrapper.appendChild(
            picker
        );


        emojiBtn.parentElement.appendChild(
            emojiWrapper
        );


        /*
        ======================================
        INSERT EMOJI INTO TEXTAREA
        ======================================
        */

        function insertEmoji(emoji) {

            diaryContent.focus();


            const start =
                diaryContent.selectionStart;

            const end =
                diaryContent.selectionEnd;


            const currentText =
                diaryContent.value;


            diaryContent.value =
                currentText.substring(
                    0,
                    start
                ) +
                emoji +
                currentText.substring(
                    end
                );


            /*
            Move cursor after emoji
            */

            const newPosition =
                start + emoji.length;


            diaryContent.setSelectionRange(
                newPosition,
                newPosition
            );


            /*
            Update word count
            */

            diaryContent.dispatchEvent(
                new Event("input")
            );

        }


        /*
        ======================================
        OPEN / CLOSE EMOJI PICKER
        ======================================
        */

        emojiBtn.addEventListener(
            "click",
            function (event) {

                event.stopPropagation();


                if (
                    emojiWrapper.style.display ===
                    "none"
                ) {

                    emojiWrapper.style.display =
                        "block";

                } else {

                    emojiWrapper.style.display =
                        "none";

                }

            }
        );


        /*
        ======================================
        CLOSE WHEN CLICKING OUTSIDE
        ======================================
        */

        document.addEventListener(
            "click",
            function (event) {

                if (
                    !emojiWrapper.contains(
                        event.target
                    ) &&
                    !emojiBtn.contains(
                        event.target
                    )
                ) {

                    emojiWrapper.style.display =
                        "none";

                }

            }
        );

    }


    /*
    ==========================================
    VISIBILITY ICON
    ==========================================
    */

    if (
        visibilityInput &&
        visibilityIcon
    ) {

        visibilityInput.addEventListener(
            "change",
            function () {

                if (this.value === "public") {

                    visibilityIcon.className =
                        "fa-solid fa-globe";

                    visibilityIcon.style.color =
                        "var(--primary)";

                } else {

                    visibilityIcon.className =
                        "fa-solid fa-lock";

                    visibilityIcon.style.color =
                        "var(--text-secondary)";

                }

            }
        );

    }


    /*
    ==========================================
    CURRENT DIARY DATE
    ==========================================
    */

    if (diaryDate) {

        const today =
            new Date();


        const formattedDate =
            today.toLocaleDateString(
                "en-US",
                {
                    month: "long",
                    day: "numeric",
                    year: "numeric"
                }
            );


        diaryDate.textContent =
            formattedDate;

    }

});