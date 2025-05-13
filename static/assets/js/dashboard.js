document.addEventListener("DOMContentLoaded", function () {
    // Sidebar navigation active state toggle
    const sidebarItems = document.querySelectorAll(".sidebar ul li");
    sidebarItems.forEach(item => {
        item.addEventListener("click", function () {
            sidebarItems.forEach(i => i.classList.remove("active"));
            this.classList.add("active");
        });
    });

    // Create Product button alert
    const createBtn = document.querySelector(".create-btn");
    createBtn.addEventListener("click", function () {
        alert("Redirecting to Create Product Page...");
    });

    // View Details button alert
    const viewBtns = document.querySelectorAll(".view-btn");
    viewBtns.forEach(btn => {
        btn.addEventListener("click", function () {
            alert("Viewing order details...");
        });
    });
});
