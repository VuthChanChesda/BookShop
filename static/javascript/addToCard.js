
    // Wait for the DOM to load
    document.addEventListener('DOMContentLoaded', function() {
        // Get the container that holds all the buttons
        const addToCard = document.querySelectorAll('#add-to-card');

        addToCard.forEach(button => {

            // Get the product ID from the button's data attribute
            const bookId = button.getAttribute('data-book-id');


            // Check if the item is already in the cart
            fetch(`/books/is_in_cart/${bookId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.in_cart) {
                    button.textContent = 'Already in Cart';
                    button.disabled = true;
                }
            })
            .catch(error => console.error('Error:', error));

            // Add a single event listener to the container
            button.addEventListener('click', function(event) {
                // Check if the clicked element is an "Add to Cart" button
                    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

                    // Send an AJAX request to add the product to the cart
                    fetch(`/books/add_to_cart/${bookId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrftoken  // Include CSRF token for security
                        },
                        body: JSON.stringify({ quantity: 1 })  // Send additional data if needed
                        // cache: 'force-cache'  // Use cache if available

                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            button.textContent = 'Already in Cart';
                            button.disabled = true;
                        } else {
                            alert('Failed to add item to cart: ' + data.error);
                        }
                    })
                    .catch(error => console.error('Error:', error));
                
            });
            
        });

    });
