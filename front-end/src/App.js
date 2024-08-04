import React, { useState, useEffect } from 'react';
import BookCard from './components/BookCard/BookCard.jsx';
import SearchBar from './components/SearchBar/SearchBar.jsx';
import Loader from './components/Loader/Loader.jsx';
import './App.css';
import ChatBot from './components/ChatBot/ChatBot.jsx'
import AuthButton from './components/AuthButton/AuthButton.jsx'
import FilterButton from './components/FilterButton/FilterButton.jsx';

const App = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [authentication, setauthentication] = useState(true);
  

  useEffect(() => {
    fetchBooks();
  }, []);

  // All book fetching
  const fetchBooks = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/books');
      const data = await response.json();
      setBooks(data);
    } catch (error) {
      console.error('Error fetching books:', error);
    } finally {
      setLoading(false);
    }
  };

  // search book fetching
  const searchBooks = async (query) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/books/${query}`);
      const data = await response.json();
      setBooks(data);
    } catch (error) {
      console.error('Error searching books:', error);
    } finally {
      setLoading(false);
    }
  };

  //function to handle filter change
    const handleFilterChange = (filteredBooks) => {
      setBooks(filteredBooks);
    };

  const chatQuery = async (query) => {
    try {
      const response = await fetch(`http://localhost:8000/chat_with_bot?user_query=${query}`);
      const data = await response.text();
      return data; 
    } catch (error) {
      console.error('Error with chat:', error);
      return "Error: Could not get a response."; 
    }
  };

  return (
    <div className="container">
      <h1 className="page-title">Library</h1>
      <h2><AuthButton onClick={""}/> </h2>
      <div style={{"height":"0.75px", "background-color": "#EAEFF5"}}></div>
        <SearchBar onSearch={searchBooks} />
        <FilterButton onFilterChange={handleFilterChange}/> 
      {loading ? (
        <Loader />
      ) : (
        <div className="book-gallery">
          {books ? ( // if not null
            Array.isArray(books) ? ( //if its a list of books
              books.length > 0 ? (   // vvv
                books.map((book) => ( // map it
                  <BookCard key={book.id} book={book} />
                ))
              ) : (
                <p>No books found.</p>
              )
            ) : (
              <BookCard key={books.id} book={books} /> //else just display the singular book
            )
          ) : (
            <p>No books found.</p>// if its neither an array or object then no books found
          )}
        </div>
      )}
    <ChatBot onSend={chatQuery} />
    </div>
  );
};

export default App;

