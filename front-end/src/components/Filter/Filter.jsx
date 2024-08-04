import React from 'react';

const Filter = ({ onFilterChange }) => {
  const handleFilterChange = async (event) => {
    const filter = event.target.value;
    let url = '';

    switch (filter) {
      case 'rating_desc':
        url = 'http://localhost:8000/books/sorted/rating_desc';
        break;
      case 'rating_asc':
        url = 'http://localhost:8000/books/sorted/rating_asc';
        break;
      case 'year_desc':
        url = 'http://localhost:8000/books/sorted/year_desc';
        break;
      case 'year_asc':
        url = 'http://localhost:8000/books/sorted/year_asc';
        break;
      default:
        return;
    }

    try {
      const response = await fetch(url);
      const data = await response.json();
      onFilterChange(data);
    } catch (error) {
      console.error('Error fetching filtered books:', error);
    }
  };

  return (
    <div className="filter-component">
      <label htmlFor="filter-select">Sort By: </label>
      <select id="filter-select" onChange={handleFilterChange}>
        <option value="">Select</option>
        <option value="rating_desc">Highest Rated</option>
        <option value="rating_asc">Lowest Rated</option>
        <option value="year_desc">Newest</option>
        <option value="year_asc">Oldest</option>
      </select>
    </div>
  );
};

export default Filter;
