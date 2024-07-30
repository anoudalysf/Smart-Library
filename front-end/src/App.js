import React, { useState, useEffect } from 'react';
import BookCard from './components/BookCard/BookCard.jsx';
import SearchBar from './components/SearchBar/SearchBar.jsx';
import Loader from './components/Loader/Loader.jsx';
import './App.css';

const App = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchBooks();
  }, []);

  const fetchBooks = async (query = '') => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/books/?query=${query}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      const data = await response.json();
      setBooks(data);
    } catch (error) {
      console.error('Failed to fetch books:', error);
      alert('Failed to fetch books: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">Books Books Books!</h1>
      <SearchBar onSearch={fetchBooks} />
      {loading ? (
        <Loader />
      ) : (
        <div id="book-gallery" className="book-gallery">
          {books.map((book) => (
            <BookCard key={book.id} book={book} />
          ))}
        </div>
      )}
    </div>
  );
};

export default App;
