document.addEventListener("scroll", function () {
    let card = document.getElementById("staticCard");
    if (window.scrollY > 50) {
        card.classList.add("scrolled");
    } else {
        card.classList.remove("scrolled");
    }
});

document.addEventListener("DOMContentLoaded", function () {
    // Select all subscribe buttons
    document.querySelectorAll(".subscribe-btn").forEach(button => {
        button.addEventListener("click", function () {
            // Get plan details from button data attributes
            const name = this.getAttribute("data-name");
            const price = this.getAttribute("data-price");
            const duration = this.getAttribute("data-duration");
            const devices = this.getAttribute("data-devices");
            const validity = this.getAttribute("data-validity");

            // Update modal with plan details
            document.getElementById("planName").innerText = name;
            document.getElementById("planAmount").innerText = price;
            document.getElementById("planDuration").innerText = duration;
            document.getElementById("planDevices").innerText = devices;
            document.getElementById("planValidity").innerText = validity;

            // Show modal
            new bootstrap.Modal(document.getElementById("mpesaModal")).show();
        });
    });
});


// Function to send payment request
function initiateMpesaPayment(mpesaNumber, amount, planName) {
    fetch("/process_mpesa_payment/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCSRFToken()  // Ensure CSRF protection
        },
        body: JSON.stringify({
            phone_number: mpesaNumber,
            amount: amount,
            plan_name: planName
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            alert("Payment request sent. Please check your M-Pesa phone.");
        } else {
            alert("Payment failed: " + data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}

// Function to get CSRF token from cookies
function getCSRFToken() {
    return document.cookie.split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
}
