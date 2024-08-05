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
  const [userid, setUserid] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const [likedBooks, setLikedBooks] = useState([]);

  
  useEffect(() => {
    const token = localStorage.getItem('token');
    const storedUsername = localStorage.getItem('username');
    const storedRole = localStorage.getItem('role');
    const storedUserid = localStorage.getItem('user_id');
    console.log("Stored role on load:", storedRole);
    if (token && storedUsername && storedRole && storedUserid) {
      setIsAuthenticated(true);
      setUsername(storedUsername);
      setRole(storedRole);
      setUserid(storedUserid);
      fetchLikedBooks(storedUserid);
    }
    fetchBooks();

  
    // redirect non-admin users away from the admin panel page
    if (location.pathname === '/admin' && storedRole !== 'Admin') {
      navigate('/');
    }
  }, [location.pathname, navigate]);

  const setAuth = async (username, user_id, role) => {
    console.log("Setting auth with role:", role);
    if (username && role) {
      setIsAuthenticated(true);
      setUsername(username);
      setRole(role);
      setUserid(user_id);
      await fetchLikedBooks(user_id); //fetch the liked books when logged in then fetch all books so the likes show upon login
      fetchBooks();
    } else { //else reset everything
      setIsAuthenticated(false);
      setUsername('');
      setRole('');
      setUserid('');
      navigate('/');
      setLikedBooks([]);
      fetchBooks(); 
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

  const fetchLikedBooks = async (user_id) => {
    if (!user_id) {
      alert('You need to be logged in to view liked books.');
      return;
    }
    try {
      const response = await fetch(`http://localhost:8000/user_preferences/${user_id}`);
      const data = await response.json();
      setLikedBooks(data);
      handleFilterChange(data); // Update books state with liked books
    } catch (error) {
      console.error('Error fetching liked books:', error);
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

    const handleLike = async (book_id, isLiked) => {
      if (!isAuthenticated) {
        alert("You need to be logged in to like books.");
        return;
      }
      try {
        const response = await fetch('http://localhost:8000/user_preferences/', {
          method: isLiked ? 'DELETE' : 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user_id: userid, book_id })
        });
  
        if (response.ok) {
          const updatedLikedBooks = isLiked
            ? likedBooks.filter(book => book.book_id !== book_id)
            : [...likedBooks, { book_id }];
          setLikedBooks(updatedLikedBooks);
        } else {
          console.error('Failed to like/unlike book');
        }
      } catch (error) {
        console.error('Error liking/unliking book:', error);
      }
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
            <SearchBar onSearch={searchBooks} onFilterChange={handleFilterChange} onLikedBooksFetch={() => fetchLikedBooks(userid)}/>
            {loading ? (
              <Loader />
            ) : (
              <div className="book-gallery">
                {books ? ( // if not null
                  Array.isArray(books) ? ( //if its a list of books
                    books.length > 0 ? (   // vvv
                      books.map((book) => ( // map it
                        <BookCard key={book.id} book={book} onLike={handleLike} likedBooks={likedBooks}/>
                      ))
                    ) : (
                      <p>No books found.</p>
                    )
                  ) : (
                    <BookCard key={books.id} book={books} onLike={handleLike} likedBooks={likedBooks}/> //else just display the singular book
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

