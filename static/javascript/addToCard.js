
function attachEventListeners() {

    const addToCardButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCardButtons.forEach(button => {

        const bookId = button.getAttribute('data-book-id');
        if (!bookId) {
            console.error('Book ID not found');
            return;
        }

        // Check if the item is already in the cart
        fetch(`/books/is_in_cart/${bookId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.in_cart) { // in_cart is a boolean value we got from the server
                    button.textContent = 'Already in Cart';
                    button.disabled = true;
                    button.classList.add('disabled'); // Add the disabled class

                }
            })
            .catch(error => console.error('Error:', error));

        // Add event listener for adding to cart
        button.addEventListener('click', function(event) {
            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/books/add_to_cart/${bookId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({ quantity: 1 })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    button.textContent = 'Already in Cart';
                    button.disabled = true;
                    button.classList.add('disabled'); // Add the disabled class
                    updateCartItemCount();  // Update cart item count
                } else {
                    alert('Failed to add item to cart: ' + data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });

}

// function updateCartItemCount() {
//     fetch('/cart/item_count/')
//         .then(response => response.json())
//         .then(data => {
//             const cartItemCountElement = document.querySelectorAll('.cart-item-count');
//             cartItemCountElement.forEach(card => {

//                 if (card) {
//                     if (data.count > 0) {
//                         card.textContent = data.count;
//                         card.style.display = 'inline';
//                     } else {
//                         card.style.display = 'none';
//                     }
//                 }

//             });

//         })
//         .catch(error => console.error('Error:', error));
// }

let currentCartItemCount = null;  // Store the current cart item count

function updateCartItemCount() {
    const cartItemCountElements = document.querySelectorAll('.cart-item-count');
    cartItemCountElements.forEach(card => {
        card.classList.add('loading');  // Add loading state
    });

    fetch('/cart/item_count/')
        .then(response => response.json())
        .then(data => {
            const newCount = data.count;
            if (newCount !== currentCartItemCount) {  // Only update if the count has changed
                currentCartItemCount = newCount;  // Update the current count
                cartItemCountElements.forEach(card => {
                    if (card) {
                        if (newCount > 0) {
                            card.textContent = newCount;
                            card.classList.remove('hidden');
                        } else {
                            card.classList.add('hidden');
                        }
                    }
                });
            }
        })
        .catch(error => console.error('Error:', error))
        .finally(() => {
            cartItemCountElements.forEach(card => {
                card.classList.remove('loading');  // Remove loading state
            });
        });
}



// Attach functions to the window object to make them globally accessible
window.attachEventListeners = attachEventListeners;
window.updateCartItemCount = updateCartItemCount;

// Wait for the DOM to load and attach event listeners
document.addEventListener('DOMContentLoaded', function() {
    attachEventListeners();
    updateCartItemCount();
});
