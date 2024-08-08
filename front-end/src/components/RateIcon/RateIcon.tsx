import React from 'react';

interface RateIconProps { 
  rating: number;
}

const RateIcon: React.FC<RateIconProps> = ({ rating }) => {
  const getFillPercentage = (): string => {
    if (rating > 4) return '100%';
    if (rating > 3) return '75%';
    if (rating > 2) return '50%';
    if (rating > 1) return '25%';
    if (rating > 0) return '10%';
    return '0%';
  };

  const fillPercentage = getFillPercentage();

  return (
    <svg fill="#000000" width="24" height="24" viewBox="0 0 24 24" id="star" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="grad1" x1="0" y1="1" x2="0" y2="0">
          <stop offset={fillPercentage} stopColor="yellow" />
          <stop offset={fillPercentage} stopColor="gray" />
        </linearGradient>
      </defs>
      <path id="primary" d="M22,9.81a1,1,0,0,0-.83-.69l-5.7-.78L12.88,3.53a1,1,0,0,0-1.76,0L8.57,8.34l-5.7.78a1,1,0,0,0-.82.69,1,1,0,0,0,.28,1l4.09,3.73-1,5.24A1,1,0,0,0,6.88,20.9L12,18.38l5.12,2.52a1,1,0,0,0,.44.1,1,1,0,0,0,1-1.18l-1-5.24,4.09-3.73A1,1,0,0,0,22,9.81Z" fill="url(#grad1)" />
    </svg>
  );
};

export default RateIcon;
