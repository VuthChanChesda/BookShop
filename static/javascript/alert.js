document.addEventListener('DOMContentLoaded', function () {
    const alertContainer = document.getElementById('alert-container');

    // Check if the success message exists in sessionStorage
    const successMessage = sessionStorage.getItem('paymentSuccessMessage');
    if (successMessage) {
        // Create a Bootstrap alert
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.role = 'alert';
        alert.innerHTML = `
            ${successMessage}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // Append the alert to the alert container
        alertContainer.appendChild(alert);

        // Remove the message from sessionStorage to prevent it from showing again
        sessionStorage.removeItem('paymentSuccessMessage');
    }
});