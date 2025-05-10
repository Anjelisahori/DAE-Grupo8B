fetch('/api/books/')
  .then(response => response.json())
  .then(data => {
    const container = document.getElementById('book-list');
    data.forEach(book => {
      const div = document.createElement('div');
      div.className = 'book-card';
      div.innerHTML = `
        <h3>${book.title} 📖</h3>
        <p><strong>Author:</strong> ${book.author__name}</p>
        <p><strong>ISBN:</strong> ${book.isbn}</p>
        ${book.publication_date ? `<p><strong>Published:</strong> ${book.publication_date}</p>` : ''}
        <p>${book.summary.substring(0, 100)}...</p>
      `;
      container.appendChild(div);
    });
  })
  .catch(error => {
    console.error('Error fetching books:', error);
  });
