import React, { useState, ChangeEvent, FormEvent } from 'react';
import styles from './UpdateModal.module.css';

interface Book {
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

interface UpdateModelProp{
  book: Book;
  onClose: () => void;
  onSave: (updatedBook: Book) => void;
}

const UpdateModal: React.FC<UpdateModelProp> = ({ book, onClose, onSave }) => {
  const [updatedBook, setUpdatedBook] = useState<Book>({ ...book });

  const handleChange = (e: ChangeEvent<HTMLInputElement| HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setUpdatedBook((prevBook) => ({
      ...prevBook,
      [name]: value,
    }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSave(updatedBook);
  };

  return (
    <div className={styles.modal}>
      <div className={styles.modalContent}>
        <span className={styles.close} onClick={onClose}>&times;</span>
        <h2>Update Book</h2>
        <form onSubmit={handleSubmit} className={styles.updateModalForm}>
          <label>
            Title:
            <input
              type="text"
              name="title"
              value={updatedBook.title}
              onChange={handleChange}
            />
          </label>
          <label>
            Authors:
            <input
              type="text"
              name="authors"
              value={updatedBook.authors}
              onChange={handleChange}
            />
          </label>
          <label>
            Published Year:
            <input
              type="number"
              name="published_year"
              value={updatedBook.published_year}
              onChange={handleChange}
            />
          </label>
          <label>
            Description:
            <textarea
              name="description"
              value={updatedBook.description}
              onChange={handleChange}
            />
          </label>
          <label>
            Categories:
            <input
              type="text"
              name="categories"
              value={updatedBook.categories}
              onChange={handleChange}
            />
          </label>
          <label>
            Average Rating:
            <input
              type="number"
              name="average_rating"
              step="0.1"
              value={updatedBook.average_rating}
              onChange={handleChange}
            />
          </label>
          <label>
            Thumbnail:
            <input
              type="text"
              name="thumbnail"
              value={updatedBook.thumbnail || ''}
              onChange={handleChange}
            />
          </label>
          <label>
            Number of Pages:
            <input
              type="number"
              name="num_pages"
              value={updatedBook.num_pages || ''}
              onChange={handleChange}
            />
          </label>
          <label>
            Ratings Count:
            <input
              type="number"
              name="ratings_count"
              value={updatedBook.ratings_count || ''}
              onChange={handleChange}
            />
          </label>
          <button type="submit">Save</button>
        </form>
      </div>
    </div>
  );
};

export default UpdateModal;
