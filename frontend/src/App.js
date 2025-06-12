import React, { useContext } from 'react'; // Added useContext
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ProductListPage from './pages/ProductListPage';
import ProductDetailPage from './pages/ProductDetailPage';
import CartPage from './pages/CartPage'; // Import CartPage
import { CartContext } from './contexts/CartContext'; // Import CartContext for item count
import './App.css';
import './assets/css/main.css';

function App() {
  const { cartItems } = useContext(CartContext); // Get cartItems for count

  const cartItemCount = cartItems.reduce((count, item) => count + item.quantity, 0);

  return (
    <Router>
      <div className="App">
        <nav style={{ padding: '1rem', background: '#f0f0f0', marginBottom: '1rem', display: 'flex', justifyContent: 'space-between' }}>
          <div>
            <Link to="/" style={{ marginRight: '1rem' }}>Home (Products)</Link>
            {/* Other nav links can go here, e.g., Categories */}
          </div>
          <div>
            <Link to="/cart" style={{ marginRight: '1rem' }}>
              Cart {cartItemCount > 0 && `(${cartItemCount})`}
            </Link>
            {/* Login/Register/Profile links will go here */}
          </div>
        </nav>
        <div style={{ padding: '1rem' }}>
          <Routes>
            <Route path="/" element={<ProductListPage />} />
            <Route path="/products/:productId" element={<ProductDetailPage />} />
            <Route path="/cart" element={<CartPage />} /> {/* Add route for CartPage */}
            {/* <Route path="/checkout" element={<CheckoutPage />} /> */} {/* Placeholder for checkout */}
          </Routes>
        </div>
        <footer style={{ padding: '1rem', background: '#f0f0f0', marginTop: '1rem', textAlign: 'center' }}>
          <p>&copy; 2024 Cosmetics Store</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
