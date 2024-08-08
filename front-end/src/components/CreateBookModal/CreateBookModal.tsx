import React, { useState, ChangeEvent, FormEvent } from 'react';
import styles from './CreateBookModal.module.css';

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

interface CreateBookModalProps {
    onClose: () => void;
    onSave: (newBook: BookCreate) => void;
  }

const CreateBookModal: React.FC<CreateBookModalProps> = ({ onClose, onSave }) => {
    const [newBook, setNewBook] = useState<BookCreate>({
        title: '',
        authors: '',
        published_year: undefined,
        description: '',
        categories: '',
        average_rating: undefined,
        thumbnail: '',
        num_pages: undefined,
        ratings_count: undefined,
      });

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setNewBook((prevBook) => ({
      ...prevBook,
      [name]: value,
    }));
  };

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSave(newBook);
  };

  return (
    <div className={styles.modal}>
      <div className={styles.modalContent}>
        <span className={styles.close} onClick={onClose}>&times;</span>
        <h2>Create Book</h2>
        <form onSubmit={handleSubmit} className={styles.createModalForm}>
          <label>
            Title:
            <input
              type="text"
              name="title"
              value={newBook.title}
              onChange={handleChange}
            />
          </label>
          <label>
            Authors:
            <input
              type="text"
              name="authors"
              value={newBook.authors}
              onChange={handleChange}
            />
          </label>
          <label>
            Published Year:
            <input
              type="number"
              name="published_year"
              value={newBook.published_year || ''}
              onChange={handleChange}
            />
          </label>
          <label>
            Description:
            <textarea
              name="description"
              value={newBook.description}
              onChange={handleChange}
            />
          </label>
          <label>
            Categories:
            <input
              type="text"
              name="categories"
              value={newBook.categories}
              onChange={handleChange}
            />
          </label>
          <label>
            Average Rating:
            <input
              type="number"
              name="average_rating"
              step="0.1"
              value={newBook.average_rating || ''}
              onChange={handleChange}
            />
          </label>
          <label>
            Thumbnail:
            <input
              type="text"
              name="thumbnail"
              value={newBook.thumbnail || ''}
              onChange={handleChange}
            />
          </label>
          <label>
            Number of Pages:
            <input
              type="number"
              name="num_pages"
              value={newBook.num_pages || ''}
              onChange={handleChange}
            />
          </label>
          <label>
            Ratings Count:
            <input
              type="number"
              name="ratings_count"
              value={newBook.ratings_count || ''}
              onChange={handleChange}
            />
          </label>
          <button type="submit">Create</button>
        </form>
      </div>
    </div>
  );
};

export default CreateBookModal;