import React, { useContext } from 'react';
import { CartContext } from '../contexts/CartContext';

const AddToCartButton = ({ product, quantity = 1 }) => {
  const { addToCart } = useContext(CartContext);

  const handleAddToCart = () => {
    addToCart(product, quantity);
    // Optionally, add some user feedback like a toast notification
    alert(`${product.name} added to cart!`);
  };

  return (
    <button onClick={handleAddToCart} disabled={product.stock === 0}>
      {product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}
    </button>
  );
};

export default AddToCartButton;
