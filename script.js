async function fetchBooks() {
    try {
        console.log('Fetching books...');
        const response = await fetch('http://localhost:8000/books/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('Response received:', response);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const books = await response.json();
        console.log('Books:', books);
        displayBooks(books);
    } catch (error) {
        console.error('Failed to fetch books:', error);
        window.alert('Failed to fetch books: ' + error.message);
    }
}

function displayBooks(books) {
    const container = document.getElementById('book-gallery');
    const colors = ['#ffadad', '#ffd6a5', '#fdffb6', '#caffbf', '#9bf6ff', '#a0c4ff', '#bdb2ff', '#ffc6ff'];
    
    books.forEach((book, index) => {
        const card = document.createElement('div');
        card.className = 'book-item';
        card.style.backgroundColor = colors[index % colors.length];
        card.innerHTML = `
            <div class="cover-photo">
                <img src="${book.thumbnail}" alt="${book.title}" />
            <h2 style="font-size: 1.25em;"class="book-title">${book.title}</h2>
            <p class="book-title"><strong>Author:</strong> ${book.authors}</p>
            <p style="font-size: 0.85em;class="book-title"><strong>Published:</strong> ${book.published_year}</p>
        `;
        container.appendChild(card);
    });
}

fetchBooks();
