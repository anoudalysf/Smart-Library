import React, { useState } from "react";
import RateIcon from "../RateIcon/RateIcon";
import styles from "../BookCard/BookCard.module.css"

interface LikeIconProps {
  onClick: () => void;
  isLiked: boolean;
}

const LikeIcon: React.FC<LikeIconProps> = ({ onClick, isLiked }) => {
  return(
    <svg width="24" height="24" viewBox="0 0 24 24" fill={isLiked ? "#FF529A" : "#AFB1B6"} xmlns="http://www.w3.org/2000/svg" onClick={onClick}>
      <mask id="mask0_1_1877" style={{"maskType":"luminance"}} maskUnits="userSpaceOnUse" x="2" y="2" width="21" height="21">
      <path fillRule="evenodd" clipRule="evenodd" d="M2 2.99988H22.4725V22.5009H2V2.99988Z" fill="white"/>
      </mask>
      <g mask="url(#mask0_1_1877)">
      <path fillRule="evenodd" clipRule="evenodd" d="M3.82371 12.123C5.22571 16.485 10.7647 20.012 12.2367 20.885C13.7137 20.003 19.2927 16.437 20.6497 12.127C21.5407 9.341 20.7137 5.812 17.4277 4.753C15.8357 4.242 13.9787 4.553 12.6967 5.545C12.4287 5.751 12.0567 5.755 11.7867 5.551C10.4287 4.53 8.65471 4.231 7.03771 4.753C3.75671 5.811 2.93271 9.34 3.82371 12.123ZM12.2377 22.501C12.1137 22.501 11.9907 22.471 11.8787 22.41C11.5657 22.239 4.19271 18.175 2.39571 12.581C2.39471 12.581 2.39471 12.58 2.39471 12.58C1.26671 9.058 2.52271 4.632 6.57771 3.325C8.48171 2.709 10.5567 2.98 12.2347 4.039C13.8607 3.011 16.0207 2.727 17.8867 3.325C21.9457 4.634 23.2057 9.059 22.0787 12.58C20.3397 18.11 12.9127 22.235 12.5977 22.408C12.4857 22.47 12.3617 22.501 12.2377 22.501Z"/>
      </g>
      <path fillRule="evenodd" clipRule="evenodd" d="M18.1537 10.6249C17.7667 10.6249 17.4387 10.3279 17.4067 9.9359C17.3407 9.1139 16.7907 8.4199 16.0077 8.1669C15.6127 8.0389 15.3967 7.6159 15.5237 7.2229C15.6527 6.8289 16.0717 6.6149 16.4677 6.7389C17.8307 7.1799 18.7857 8.3869 18.9027 9.8139C18.9357 10.2269 18.6287 10.5889 18.2157 10.6219C18.1947 10.6239 18.1747 10.6249 18.1537 10.6249Z"/>
    </svg>

  )
}

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

interface BookProps {
  book: Book;
  onLike: (book_id: number, isLiked: boolean) => void;
  likedBooks: Book[];
}

interface BookFrontBackProps {
  book: Book;
}

const BookFront: React.FC<BookFrontBackProps> = ({ book }) => {
  return (
      <img src={book.thumbnail} alt={book.title} />
  );
};

const BookBack: React.FC<BookFrontBackProps> = ({ book }) => {
  return (
      <h2 className={styles.description}>{book.description}</h2>
  );
};

const BookCard: React.FC<BookProps> = ({ book, onLike, likedBooks }) => {
  const [isFlipped, setFlipped] = useState(false);

  const handleFlip = () => {
    setFlipped(!isFlipped);
  };

  const isLiked = likedBooks.some(likedBook => likedBook.book_id === book.book_id);

  return (
    <div className={styles.item}>
      <h2 className={styles.title}>{book.title} <LikeIcon onClick={() => onLike(book.book_id, isLiked)} isLiked={isLiked} /></h2>
      <div className={styles.multipleTitles}>
        <p className={styles.subtitle}>{book.authors}</p>
        <p className={styles.subtitle}>{book.published_year}</p>
      </div>
      <div className={styles.coverPhoto}>
        <div className={`${styles.flipCard} ${isFlipped ? styles.flipped : ""}`} onClick={handleFlip}>
          <div className={styles.flipCardInner}>
            <div className={styles.flipCardFront}>
              <BookFront book={book} />
            </div>
            <div className={styles.flipCardBack}>
              <BookBack book={book} />
              </div>
            </div>
          </div>
      </div>
      <div className={styles.multipleTitles}>
      <p className={styles.subtitle}>{book.categories}</p>
      <div className={styles.rating}>
      <p className={styles.subtitle}>{book.average_rating}
          <RateIcon rating={book.average_rating} /> </p>
        </div>
      </div>
    </div>
  );
};

export default BookCard;
