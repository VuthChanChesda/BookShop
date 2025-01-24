function updateURL(value) {
    if (value) {
        history.pushState({}, '', `?q=${encodeURIComponent(value)}`);
    } else {
        history.pushState({}, '', window.location.pathname);
    }
 }
 
 document.addEventListener('DOMContentLoaded', function() {

    // Get the value of the 'q' query parameter from the URL, or set it to an empty string if it doesn't exist
    let query = new URLSearchParams(window.location.search).get('q') || '';
 
    const searchInput = document.querySelectorAll('#search-input');
    const resultsContainer = document.querySelector('#search-results');
    const searchQueryUrlShow = document.querySelector('#search-query');
 
    // Initial setup
    searchInput.value = query;
 
    // Add input event listener
    searchInput.forEach(element => {

        element.addEventListener('input', function() {
            // Update query and URL
            query = element.value;
            updateURL(query);
     
            // Perform search
            performSearch(query);
        });
        
    });
    
    // searchInput.addEventListener('input', function() {
    //     // Update query and URL
    //     query = searchInput.value;
    //     updateURL(query);
 
    //     // Perform search
    //     performSearch(query);
    // });
 
    function performSearch(searchQuery) {

            const p = document.createElement('p');
            p.textContent = `Search results for "${searchQuery}"`;
            p.classList.add('search-query');
            searchQueryUrlShow.innerHTML = '';
            searchQueryUrlShow.appendChild(p);



        if (searchQuery.length > 2) {
            const url = new URL('/api/search/', window.location.origin);
            url.searchParams.append('q', searchQuery);
 
            fetch(url)
                .then(response => response.json())
                .then(data => {
                        // Clear previous results
                    resultsContainer.innerHTML = '';
 
                    if(data.length > 0) {

                        data.forEach(book => { // Loop through the array of book objects
                            const bookElement = document.createElement('div');
                            if(data.length === 1) {
                                bookElement.classList.add('col-md-12', 'col-lg-12', 'mb-3');
                            } else {
                                bookElement.classList.add('col-md-6', 'col-lg-5', 'mb-3');
                            }
                            bookElement.innerHTML = `
                                <div class="card" id="book-card">   
                                    <div class="card-body card-body-show-by-category">
                                        <a href="/books/${book.slug}">
                                            <img src="${book.cover_image}" class="d-block mx-auto" alt="${book.title}">
                                        </a>
                                        <h6 class="card-title mt-3 truncate">${book.title}</h6>
                                        <p class="card-text text-muted">${book.author}</p>
                                        <p>$${book.price}</p>
                                        <div class="d-flex justify-content-center">
                                            <button class="btn-Add-to-card-show-by-category mb-3">Add to Cart</button>
                                        </div>
                                    </div>
                                </div>
                            `;
                            resultsContainer.appendChild(bookElement);
                        });
                    }
                    else {
                        resultsContainer.innerHTML = '<p class="text-center"><span> No results found</span></p>';
                    }


                });
        } else {
            resultsContainer.innerHTML = '';
        }
    }
 
    // Perform initial search if query exists in URL
    if (query) {
        performSearch(query);
    }
    
 });