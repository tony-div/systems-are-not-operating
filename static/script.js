// Initialize event listeners after header is loaded
document.addEventListener("DOMContentLoaded", function () {
    // Dynamically load the header
    fetch("header.html")
      .then(response => response.text())
      .then(data => {
        document.getElementById("header-container").innerHTML = data;

        // Attach event listeners to nav links
        document.querySelectorAll('.nav-link').forEach(link => {
          link.addEventListener('click', handleNavClick);
        });
      })
      .catch(error => console.error("Error loading header:", error));
});
