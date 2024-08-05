import React, { useState, useEffect } from 'react';
import BookCard from './components/BookCard/BookCard.jsx';
import SearchBar from './components/SearchBar/SearchBar.jsx';
import Loader from './components/Loader/Loader.jsx';
import './App.css';
import ChatBot from './components/ChatBot/ChatBot.jsx'
import AuthButton from './components/AuthButton/AuthButton.jsx'
import AdminPanel from './components/AdminPanel/AdminPanel.jsx';
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation} from 'react-router-dom';


const App = () => {
  const [books, setBooks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [role, setRole] = useState('');
  const navigate = useNavigate();
  const location = useLocation();

  
  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUsername = localStorage.getItem('username');
    const storedRole = localStorage.getItem('role');
    console.log("Stored role on load:", storedRole);
    if (token && storedUsername && storedRole) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
      setRole(storedRole);
    }
    fetchBooks();

      // redirect non-admin users away from the admin panel page
      if (location.pathname === '/admin' && storedRole !== 'Admin') {
        navigate('/');
      }
    }, [location.pathname, navigate]);

  const setAuth = (username, role) => {
    console.log("Setting auth with role:", role);
    if (username && role) {
      setIsAuthenticated(true);
      setUsername(username);
      setRole(role);
    } else {
      setIsAuthenticated(false);
      setUsername('');
      setRole('');
      navigate('/');
    }
  };

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
      {isAuthenticated && <h1 className="page-title">Welcome, {username}!</h1>}
      <h2><AuthButton isAuthenticated={isAuthenticated} role={role} setAuth={setAuth} /></h2>
      <div style={{ height: "0.75px", backgroundColor: "#EAEFF5" }}></div>
      <Routes>
        <Route path="/" element={
          <>
            <SearchBar onSearch={searchBooks} onFilterChange={handleFilterChange} />
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
          </>
        } />
        <Route path="/admin" element={<AdminPanel />} />
      </Routes>
    </div>
  );
};

export default App;

