document.addEventListener('DOMContentLoaded', function () {
    const resultElement = document.getElementById('verification-result');
    const paymentData = document.getElementById('payment-data');
    const qrExpiryElement = document.getElementById('qr-expiry-message'); // Element to display QR expiry message
    const timerElement = document.getElementById('timer'); // Element to display the countdown timer
    const startTime = Date.now(); // Record the start time
    const timeoutDuration = 180; // Timeout duration in seconds (3 minutes)



    // Check if paymentData exists before accessing its attributes
    const md5Hash = paymentData ? paymentData.getAttribute('data-md5-hash') : null;

    // If md5Hash is not available, skip the payment verification logic
    if (!md5Hash) {
        console.log("No MD5 hash available. Skipping payment verification.");
        return;
    }

    // Function to update the countdown timer
    function updateTimer() {
        const elapsedTime = (Date.now() - startTime) / 1000; // Calculate elapsed time in seconds
        const remainingTime = Math.max(timeoutDuration - elapsedTime, 0); // Calculate remaining time
        const minutes = Math.floor(remainingTime / 60);
        const seconds = Math.floor(remainingTime % 60);

        // Update the timer element
        timerElement.textContent = `Time remaining: ${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;

        // Stop updating the timer if time runs out
        if (remainingTime <= 0) {
            clearInterval(timerInterval);
        }
    }

    function verifyPayment() {
        fetch(`/verify-payment/${md5Hash}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                console.log("Verification Response:", data); // Debugging
                

                // Ensure responseCode is treated as a number
                if (data.responseCode === 0) { // Payment verified successfully
                    resultElement.textContent = "Payment verified successfully!";
                    resultElement.style.color = "green";
                    qrExpiryElement.style.display = "none"; // Hide QR expiry message
                    clearInterval(timerInterval); // Stop the timer

                    sessionStorage.setItem('paymentSuccessMessage', 'Successfully purchased the book! Thank you for your order.❤️'); // Store success message in sessionStorage

                    // Redirect to the desired page after 6 seconds
                    setTimeout(() => {
                        window.location.href = "/"; // Replace "/success" with your desired URL
                    }, 6000); // Wait 2 seconds before redirecting

                } else if (data.error === "Transaction not found. Please complete the payment.") {
                    const elapsedTime = (Date.now() - startTime) / 1000; // Calculate elapsed time in seconds
                    if (elapsedTime < timeoutDuration) { // Retry for up to 3 minutes (180 seconds)
                        resultElement.textContent = "Waiting for payment...";
                        resultElement.style.color = "orange";
                        setTimeout(verifyPayment, 5000); // Retry after 5 seconds
                    } else {
                        resultElement.textContent = "Payment verification timed out. Please try again.";
                        resultElement.style.color = "red";
    
                        // Display QR expiry message
                        qrExpiryElement.textContent = "The QR code has expired. Please refresh the page to generate a new QR code.";
                        qrExpiryElement.style.color = "red";
                        qrExpiryElement.style.display = "block";
                        clearInterval(timerInterval); // Stop the timer
                    }
                } else {
                    resultElement.textContent = "Payment verification failed.";
                    resultElement.style.color = "red";
                    clearInterval(timerInterval); // Stop the timer
                }
            })
            .catch(error => {
                resultElement.textContent = "An error occurred during verification.";
                resultElement.style.color = "red";
                console.error("Error verifying payment:", error);
                clearInterval(timerInterval); // Stop the timer
            });
    }

    // Start the countdown timer
    const timerInterval = setInterval(updateTimer, 1000); // Update the timer every second

    // Start polling immediately when the page loads
    verifyPayment();
});