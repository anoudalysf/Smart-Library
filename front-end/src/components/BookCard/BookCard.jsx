import React from 'react';

const BookCard = ({ book, index}) => {
  const colors = ['#ffadad', '#ffd6a5', '#fdffb6', '#caffbf', '#9bf6ff', '#a0c4ff', '#bdb2ff', '#ffc6ff'];
  const color = colors[index % colors.length];

  return (
    <div className="book-item" style={{ backgroundColor: color }}>
      <div className="cover-photo">
        <img src={book.thumbnail} alt={book.title} />
      </div>
      <h2 className="book-title">{book.title}</h2>
      <p className="book-title"><strong>Author:</strong> {book.authors}</p>
      <p className="book-title"><strong>Published:</strong> {book.published_year}</p>
    </div>
  );
};

export default BookCard;
