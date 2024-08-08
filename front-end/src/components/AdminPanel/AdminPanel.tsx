import React, { useState, useEffect } from 'react';
import styles from './AdminPanel.module.css';
import UpdateModal from '../UpdateModal/UpdateModal';
import CreateBookModal from '../CreateBookModal/CreateBookModal';


const apiUrl = process.env.REACT_APP_API_URL as string;

interface Book {
  book_id: number;
  title: string;
  authors: string;
  published_year: number;
  description: string;
  categories: string;
  average_rating: number;
}

interface BookCreate {
  title: string;
  authors: string;
  published_year?: number;
  description: string;
  categories: string;
  average_rating?: number;
  thumbnail?: string;
  num_pages?: number;
  ratings_count?: number;
}

const DeleteIcon: React.FC = () => {
  return (
      <svg width="21" height="19" viewBox="0 0 21 19" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path fill-rule="evenodd" clip-rule="evenodd" d="M8.27254 11.9832C8.11475 11.9832 7.95695 11.9254 7.83697 11.8091C7.59617 11.5771 7.59617 11.2019 7.83697 10.9699L11.7752 7.17623C12.016 6.94427 12.4055 6.94427 12.6463 7.17623C12.8871 7.40819 12.8871 7.78344 12.6463 8.01539L8.7081 11.8091C8.58812 11.9254 8.43033 11.9832 8.27254 11.9832Z" fill="#FF0000"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M12.2124 11.9855C12.0546 11.9855 11.8968 11.9277 11.7768 11.8114L7.83532 8.01375C7.59453 7.78179 7.59453 7.40654 7.83532 7.17458C8.07694 6.94262 8.46648 6.94262 8.70646 7.17458L12.6479 10.9722C12.8887 11.2042 12.8887 11.5794 12.6479 11.8114C12.5279 11.9277 12.3693 11.9855 12.2124 11.9855Z" fill="#FF0000"/>
        <path fill-rule="evenodd" clip-rule="evenodd" d="M6.68024 2.77084C4.60102 2.77084 3.25734 4.1428 3.25734 6.26684V12.7332C3.25734 14.8572 4.60102 16.2292 6.68024 16.2292H13.8038C15.8839 16.2292 17.2284 14.8572 17.2284 12.7332V6.26684C17.2284 4.1428 15.8839 2.77084 13.8046 2.77084H6.68024ZM13.8038 17.4167H6.68024C3.89507 17.4167 2.0246 15.5341 2.0246 12.7332V6.26684C2.0246 3.46593 3.89507 1.58334 6.68024 1.58334H13.8046C16.5898 1.58334 18.4611 3.46593 18.4611 6.26684V12.7332C18.4611 15.5341 16.5898 17.4167 13.8038 17.4167Z" fill="#FF0000"/>
      </svg>
  )

}

const UpdateIcon: React.FC = () => {
  return (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path fill-rule="evenodd" clip-rule="evenodd" d="M16.577 22.3686H7.753C4.312 22.3686 2 19.9536 2 16.3596V8.04562C2 4.45162 4.312 2.03662 7.753 2.03662H11.492C11.906 2.03662 12.242 2.37262 12.242 2.78662C12.242 3.20062 11.906 3.53662 11.492 3.53662H7.753C5.169 3.53662 3.5 5.30662 3.5 8.04562V16.3596C3.5 19.0986 5.169 20.8686 7.753 20.8686H16.577C19.161 20.8686 20.831 19.0986 20.831 16.3596V12.3316C20.831 11.9176 21.167 11.5816 21.581 11.5816C21.995 11.5816 22.331 11.9176 22.331 12.3316V16.3596C22.331 19.9536 20.018 22.3686 16.577 22.3686Z" fill="#41D0C8"/>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M8.86762 15.4282H11.8446C12.2246 15.4282 12.5806 15.2812 12.8496 15.0122L20.3586 7.50324C20.6666 7.19524 20.8366 6.78524 20.8366 6.34924C20.8366 5.91224 20.6666 5.50124 20.3586 5.19324L19.1416 3.97624C18.5046 3.34124 17.4686 3.34124 16.8306 3.97624L9.35762 11.4492C9.09862 11.7082 8.95162 12.0522 8.94262 12.4172L8.86762 15.4282ZM11.8446 16.9282H8.09862C7.89662 16.9282 7.70262 16.8462 7.56162 16.7012C7.42062 16.5572 7.34362 16.3622 7.34862 16.1592L7.44262 12.3802C7.46162 11.6282 7.76462 10.9212 8.29662 10.3882H8.29762L15.7706 2.91524C16.9926 1.69524 18.9796 1.69524 20.2016 2.91524L21.4186 4.13224C22.0116 4.72424 22.3376 5.51124 22.3366 6.34924C22.3366 7.18724 22.0106 7.97324 21.4186 8.56424L13.9096 16.0732C13.3586 16.6242 12.6246 16.9282 11.8446 16.9282Z" fill="#41D0C8"/>
      <path fill-rule="evenodd" clip-rule="evenodd" d="M19.7308 9.9166C19.5388 9.9166 19.3468 9.8436 19.2008 9.6966L14.6348 5.1306C14.3418 4.8376 14.3418 4.3626 14.6348 4.0696C14.9278 3.7766 15.4018 3.7766 15.6948 4.0696L20.2608 8.6366C20.5538 8.9296 20.5538 9.4036 20.2608 9.6966C20.1148 9.8436 19.9228 9.9166 19.7308 9.9166Z" fill="#41D0C8"/>
    </svg>

  )
}

const CreateIcon: React.FC = () => {
  return(
    <svg width="21" height="19" viewBox="0 0 21 19" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path fill-rule="evenodd" clip-rule="evenodd" d="M6.68024 2.77083C4.60102 2.77083 3.25734 4.14279 3.25734 6.26683V12.7332C3.25734 14.8572 4.60102 16.2292 6.68024 16.2292H13.8038C15.8839 16.2292 17.2284 14.8572 17.2284 12.7332V6.26683C17.2284 4.14279 15.8839 2.77083 13.8046 2.77083H6.68024ZM13.8038 17.4167H6.68024C3.89507 17.4167 2.0246 15.5341 2.0246 12.7332V6.26683C2.0246 3.46591 3.89507 1.58333 6.68024 1.58333H13.8046C16.5898 1.58333 18.4611 3.46591 18.4611 6.26683V12.7332C18.4611 15.5341 16.5898 17.4167 13.8038 17.4167Z" fill="#41D0C8"/>
    <path fill-rule="evenodd" clip-rule="evenodd" d="M10.8378 12.7349C10.7112 12.8483 10.5364 12.9185 10.3432 12.918C9.95673 12.918 9.64412 12.6381 9.64413 12.2922L9.64412 6.63433C9.64412 6.28839 9.95673 6.00856 10.3432 6.00856C10.7297 6.00856 11.0423 6.28839 11.0423 6.63433L11.0423 12.2922C11.043 12.4652 10.9645 12.6216 10.8378 12.7349Z" fill="#41D0C8"/>
    <path fill-rule="evenodd" clip-rule="evenodd" d="M14.0001 9.90673C13.8735 10.0201 13.6987 10.0903 13.5055 10.0897L7.17876 10.0891C6.79229 10.0891 6.47968 9.80932 6.47968 9.46338C6.48034 9.11685 6.79294 8.83702 7.17876 8.83761L13.5055 8.8382C13.892 8.8382 14.2046 9.11803 14.2046 9.46397C14.2052 9.63694 14.1261 9.79397 14.0001 9.90673Z" fill="#41D0C8"/>
    </svg>
  )
}


const AdminPanel: React.FC = () => {
  const [books, setBooks] = useState<Book[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedBook, setSelectedBook] = useState<Book | null>(null);
  const [isModalOpen, setModalOpen] = useState(false);
  const [isCreateModalOpen, setCreateModalOpen] = useState(false);

  useEffect(() => {
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

    fetchBooks();
  }, []);

  const handleDelete = async (book_id: number) => {
    try {
      const response = await fetch(`${apiUrl}/books/${book_id}`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // using token for authentication
        }
      });
      if (response.ok) {
        setBooks(books.filter(book => book.book_id !== book_id));
      } else {
        console.error('Failed to delete book');
      }
    } catch (error) {
      console.error('Error deleting book:', error);
    }
  };

  const handleUpdate = (book: Book) => {
    setSelectedBook(book);
    setModalOpen(true);
  };

  const handleSave = async (updatedBook: Book) => {
    try {
      const response = await fetch(`${apiUrl}/books/${updatedBook.book_id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}` // using the token for authentication
        },
        body: JSON.stringify(updatedBook)
      });
      if (response.ok) {
        setBooks(books.map(book => (book.book_id === updatedBook.book_id ? updatedBook : book)));
        setModalOpen(false);
      } else {
        console.error('Failed to update book');
      }
    } catch (error) {
      console.error('Error updating book:', error);
    }
  };

  const handleCreate = async (newBook: BookCreate) => {
    try {
      const response = await fetch(`${apiUrl}/books`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(newBook)
      });
      if (response.ok) {
        const createdBook = await response.json();
        setBooks([...books, createdBook]);
        setCreateModalOpen(false);
      } else {
        console.log(response);
        console.error('Failed to create book');
      }
    } catch (error) {
      console.error('Error creating book:', error);
    }
  };

  return (
    <div className={styles.adminPanelContainer}>
      <div className={styles.adminPanelHeader}>
        <h1 className={styles.adminPanelTitle}>Admin Panel</h1>
      </div>
      <div className={styles.adminPanelContent}>
      <div className={styles.booksContainer}>
        <h2>Books <button onClick={() => setCreateModalOpen(true)}><CreateIcon /></button></h2>
          {loading ? (
            <p>Loading...</p>
          ) : (
            <table>
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Authors</th>
                  <th>Published Year</th>
                  <th>Description</th>
                  <th>Categories</th>
                  <th>Average Rating</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {books.map((book) => (
                  <tr key={book.book_id}>
                    <td>{book.title}</td>
                    <td>{book.authors}</td>
                    <td>{book.published_year}</td>
                    <td className={styles.description}>{book.description}</td>
                    <td>{book.categories}</td>
                    <td>{book.average_rating}</td>
                    <td>
                      <button onClick={() => handleDelete(book.book_id)}><DeleteIcon/></button>
                      <button onClick={() => handleUpdate(book)}><UpdateIcon/></button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
        <div className={styles.usersContainer}>
          <h2>Users</h2>
          {/* gonna add the users registered and their roles here later */}
        </div>
      </div>
      {isModalOpen && selectedBook &&(
        <UpdateModal
          book={selectedBook}
          onClose={() => setModalOpen(false)}
          onSave={handleSave}
        />
      )}
      {isCreateModalOpen && (
        <CreateBookModal
          onClose={() => setCreateModalOpen(false)}
          onSave={handleCreate}/>
        )}
    </div>
  );
};

export default AdminPanel;
