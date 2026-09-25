
<script>
document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("site-modal");
    const closeButton = document.querySelector(".site-modal__close");

    if (!modal || !closeButton) return;

    function closeModal() {
        modal.classList.add("is-hidden");
    }

    closeButton.addEventListener("click", closeModal);

    modal.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });

    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            closeModal();
        }
    });
});
</script>

