import React from 'react';
import { Link } from 'react-router-dom';
import AddToCartButton from './AddToCartButton'; // Import AddToCartButton

const ProductCard = ({ product }) => {
  const imageUrl = product.image ? `http://localhost:8000${product.image}` : 'https://via.placeholder.com/150';

  return (
    <div style={{ border: '1px solid #ccc', margin: '10px', padding: '10px', width: '200px', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
      <div>
        <img src={imageUrl} alt={product.name} style={{ width: '100%', height: '150px', objectFit: 'cover' }} />
        <h3>{product.name}</h3>
        <p>${product.price}</p>
      </div>
      <div>
        <Link to={`/products/${product.id}`} style={{display: 'block', marginBottom: '5px'}}>View Details</Link>
        <AddToCartButton product={product} />
      </div>
    </div>
  );
};

export default ProductCard;
