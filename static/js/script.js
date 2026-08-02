// ================================
// DentalVision - script.js
// ================================

document.addEventListener("DOMContentLoaded", function () {

    // ==============================
    // Upload Box Click
    // ==============================

    const uploadBox = document.querySelector(".upload-box");
    const fileInput = document.querySelector("input[type='file']");

    if (uploadBox && fileInput) {

        uploadBox.addEventListener("click", function () {

            fileInput.click();

        });

    }

    // ==============================
    // Show Selected File Name
    // ==============================

    if (fileInput) {

        fileInput.addEventListener("change", function () {

            if (this.files.length > 0) {

                let fileName = this.files[0].name;

                let text = uploadBox.querySelector("h3");

                if (text) {

                    text.innerHTML = "✔ " + fileName;

                }

            }

        });

    }

    // ==============================
    // Analyze Button Loading Effect
    // ==============================

    const form = document.querySelector("form");

    const button = document.querySelector(".analyze-btn");

    if (form && button) {

        form.addEventListener("submit", function () {

            button.innerHTML = "Analyzing...";

            button.disabled = true;

        });

    }

    // ==============================
    // Smooth Fade Animation
    // ==============================

    const cards = document.querySelectorAll(".card");

    cards.forEach(function (card, index) {

        card.style.opacity = "0";

        card.style.transform = "translateY(30px)";

        setTimeout(function () {

            card.style.transition = "0.6s";

            card.style.opacity = "1";

            card.style.transform = "translateY(0px)";

        }, index * 150);

    });

});