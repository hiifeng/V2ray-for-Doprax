import React, { useState, useEffect, useContext } from 'react'; // Added useContext
import { useParams, Link } from 'react-router-dom';
import { getProductById } from '../services/api';
import AddToCartButton from '../components/AddToCartButton'; // Import AddToCartButton
// CartContext might be needed if we want to show item count in cart or similar feedback directly here
// import { CartContext } from '../contexts/CartContext';

const ProductDetailPage = () => {
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { productId } = useParams();
  const [quantity, setQuantity] = useState(1); // For selecting quantity before adding to cart

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        setLoading(true);
        const response = await getProductById(productId);
        setProduct(response.data);
        setError(null);
      } catch (err) {
        setError(err.message || 'Failed to fetch product details.');
        setProduct(null);
      } finally {
        setLoading(false);
      }
    };

    if (productId) {
      fetchProduct();
    }
  }, [productId]);

  if (loading) return <p>Loading product details...</p>;
  if (error) return <p>Error: {error}</p>;
  if (!product) return <p>Product not found.</p>;

  const imageUrl = product.image ? `http://localhost:8000${product.image}` : 'https://via.placeholder.com/300';

  return (
    <div>
      <Link to="/">Back to products</Link>
      <h2>{product.name}</h2>
      <img src={imageUrl} alt={product.name} style={{ maxWidth: '400px', marginBottom: '20px' }} />
      <p><strong>Category:</strong> {product.category ? product.category.name : 'N/A'}</p>
      <p><strong>Price:</strong> ${product.price}</p>
      <p><strong>Stock:</strong> {product.stock > 0 ? `${product.stock} available` : 'Out of stock'}</p>
      <p><strong>Description:</strong></p>
      <p>{product.description || 'No description available.'}</p>

      {product.stock > 0 && (
        <div style={{ marginTop: '10px' }}>
          <label htmlFor="quantity" style={{ marginRight: '5px' }}>Quantity:</label>
          <input
            type="number"
            id="quantity"
            value={quantity}
            min="1"
            max={product.stock}
            onChange={(e) => setQuantity(parseInt(e.target.value))}
            style={{width: '50px', marginRight: '10px'}}
          />
          <AddToCartButton product={product} quantity={quantity} />
        </div>
      )}
      {product.stock === 0 && <p>Out of stock</p>}
    </div>
  );
};

export default ProductDetailPage;
