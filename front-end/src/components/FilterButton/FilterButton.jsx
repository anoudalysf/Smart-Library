import React, { useState } from "react";
import './FilterButton.css';

const FilterButton = ({onFilterChange}) => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleFilter = () => {
        setIsOpen(!isOpen);
      };
  
      const fetchBooks = async (url) => {
        try {
          const response = await fetch(url);
          const data = await response.json();
          onFilterChange(data);
        } catch (error) {
          console.error('Error fetching filtered books:', error);
        }
      };
    
      const handleMostRated = () => {
        fetchBooks('http://localhost:8000/books/sorted/rating_desc?start=0&limit=100');
      };
    
      const handleLeastRated = () => {
        fetchBooks('http://localhost:8000/books/sorted/rating_asc?start=0&limit=100');
      };
    
      const handleYearDesc = () => {
        fetchBooks('http://localhost:8000/books/sorted/year_desc?start=0&limit=100');
      };
    
      const handleYearAsc = () => {
        fetchBooks('http://localhost:8000/books/sorted/year_asc?start=0&limit=100');
      };
    
      return (
        <div>
          <button className="filter-toggle" onClick={toggleFilter}>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path fillRule="evenodd" clipRule="evenodd" d="M10.0801 18.5928H3.77905C3.36505 18.5928 3.02905 18.2568 3.02905 17.8428C3.02905 17.4288 3.36505 17.0928 3.77905 17.0928H10.0801C10.4941 17.0928 10.8301 17.4288 10.8301 17.8428C10.8301 18.2568 10.4941 18.5928 10.0801 18.5928Z" fill="white"/>
              <path fillRule="evenodd" clipRule="evenodd" d="M19.1909 8.90039H12.8909C12.4769 8.90039 12.1409 8.56439 12.1409 8.15039C12.1409 7.73639 12.4769 7.40039 12.8909 7.40039H19.1909C19.6049 7.40039 19.9409 7.73639 19.9409 8.15039C19.9409 8.56439 19.6049 8.90039 19.1909 8.90039Z" fill="white"/>
              <mask id="mask0_1_1999" style={{"mask-type":"luminance"}} maskUnits="userSpaceOnUse" x="3" y="5" width="7" height="7">
                <path fillRule="evenodd" clipRule="evenodd" d="M3 5.00037H9.2258V11.192H3V5.00037Z" fill="white"/>
              </mask>
              <g mask="url(#mask0_1_1999)">
                <path fillRule="evenodd" clipRule="evenodd" d="M6.11276 6.5C5.22376 6.5 4.49976 7.216 4.49976 8.097C4.49976 8.977 5.22376 9.692 6.11276 9.692C7.00276 9.692 7.72576 8.977 7.72576 8.097C7.72576 7.216 7.00276 6.5 6.11276 6.5ZM6.11276 11.192C4.39676 11.192 2.99976 9.804 2.99976 8.097C2.99976 6.39 4.39676 5 6.11276 5C7.82976 5 9.22576 6.39 9.22576 8.097C9.22576 9.804 7.82976 11.192 6.11276 11.192Z" fill="white"/>
              </g>
              <path fillRule="evenodd" clipRule="evenodd" d="M17.3877 16.208C16.4977 16.208 15.7737 16.924 15.7737 17.804C15.7737 18.685 16.4977 19.4 17.3877 19.4C18.2767 19.4 18.9997 18.685 18.9997 17.804C18.9997 16.924 18.2767 16.208 17.3877 16.208ZM17.3877 20.9C15.6707 20.9 14.2737 19.511 14.2737 17.804C14.2737 16.097 15.6707 14.708 17.3877 14.708C19.1037 14.708 20.4997 16.097 20.4997 17.804C20.4997 19.511 19.1037 20.9 17.3877 20.9Z" fill="white"/>
            </svg>
          </button>
          {isOpen && (
            <div className="filter-box">
              <button className="category" onClick={handleMostRated}>Most Rated</button>
              <button className="category" onClick={handleLeastRated}>Least Rated</button>
              <button className="category" onClick={handleYearDesc}>Newest</button>
              <button className="category" onClick={handleYearAsc}>Oldest</button>
            </div>
          )}
        </div>
      );
    };

export default FilterButton;