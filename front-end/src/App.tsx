import React, { useState, useEffect } from 'react';
import BookCard from './components/BookCard/BookCard';
import SearchBar from './components/SearchBar/SearchBar';
import Loader from './components/Loader/Loader';
import './App.css';
import ChatBot from './components/ChatBot/ChatBot'
import AuthButton from './components/AuthButton/AuthButton'
import AdminPanel from './components/AdminPanel/AdminPanel';
import { BrowserRouter as Router, Route, Routes, useNavigate, useLocation} from 'react-router-dom';

const apiUrl = process.env.REACT_APP_API_URL as string;

interface Book {
  id: string;
  book_id: number;
  title: string;
  authors: string;
  published_year: number;
  description: string;
  categories: string;
  average_rating: number;
  thumbnail?: string;
  num_pages?: number;
  ratings_count?: number;
}

const App: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [username, setUsername] = useState('');
  const [role, setRole] = useState('');
  const [userid, setUserid] = useState('');
  const navigate = useNavigate();
  const location = useLocation();
  const [likedBooks, setLikedBooks] = useState<Book[]>([]);

   
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

  const setAuth = async (username: string | null, user_id: string, role: string | null) => {
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
      const response = await fetch(`${apiUrl}/books`);
      const data = await response.json();
      setBooks(data);
    } catch (error) {

      console.error('Error fetching books:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchLikedBooks = async (user_id: string) => {
    if (!user_id) {
      alert('You need to be logged in to view liked books.');
      return;
    }
    try {
      const response = await fetch(`${apiUrl}/user_preferences/${user_id}`);
      const data = await response.json();
      setLikedBooks(data);
      handleFilterChange(data); //update books state with liked books
    } catch (error) {
      console.error('Error fetching liked books:', error);
    }
  };
  

  // search book fetching
  const searchBooks = async (query: string) => {
    setLoading(true);
    try {
      const response = await fetch(`${apiUrl}/similarity?query=${query}`);
      const data = await response.json();
      setBooks(data);
    } catch (error) {
      console.error('Error searching books:', error);
    } finally {
      setLoading(false);
    }
  };

  //function to handle filter change
    const handleFilterChange = (filteredBooks: Book[]) => {
      setBooks(filteredBooks);
    };

    const handleLike = async (book_id: number, isLiked: boolean) => {
      if (!isAuthenticated) {
        alert("You need to be logged in to like books.");
        return;
      }
      try {
        const response = await fetch(`${apiUrl}/user_preferences/`, {
          method: isLiked ? 'DELETE' : 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ user_id: userid, book_id })
        });
  
        if (response.ok) {
          const updatedLikedBooks = isLiked
            ? likedBooks.filter(book => book.book_id !== book_id)
            : [...likedBooks, { book_id } as Book];
          setLikedBooks(updatedLikedBooks);
        } else {
          console.error('Failed to like/unlike book');
        }
      } catch (error) {
        console.error('Error liking/unliking book:', error);
      }
    };

    const chatQuery = async (
      query: string,
      onUpdate: (chunk: string) => void
    ): Promise<void> => {
      try {
        const response = await fetch(`${apiUrl}/chat_with_intents?user_query=${query}`
          , {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_query: query }),
          });
    
        if (!response.body) {
          onUpdate("Error: Could not get a response.");
          return;
        }
    
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
    
        let done = false;
    
        while (!done) {
          const { value, done: readerDone } = await reader.read();
          done = readerDone;
          const chunk = decoder.decode(value, { stream: true });
    
          onUpdate(chunk);
        }
      } catch (error) {
        console.error("Error with chat:", error);
        onUpdate("Error: Could not get a response.");
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
                    <BookCard book={books} onLike={handleLike} likedBooks={likedBooks}/> //else just display the singular book
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

