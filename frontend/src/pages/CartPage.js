import React, { useContext } from 'react';
import { CartContext } from '../contexts/CartContext';
import { Link } from 'react-router-dom';

const CartPage = () => {
  const { cartItems, removeFromCart, updateQuantity, getCartTotal, clearCart } = useContext(CartContext);

  if (cartItems.length === 0) {
    return (
      <div>
        <h2>Shopping Cart</h2>
        <p>Your cart is empty.</p>
        <Link to="/">Continue shopping</Link>
      </div>
    );
  }

  return (
    <div>
      <h2>Shopping Cart</h2>
      <button onClick={clearCart} style={{ marginBottom: '1rem' }}>Clear Cart</button>
      {cartItems.map(item => (
        <div key={item.id} style={{ borderBottom: '1px solid #eee', padding: '10px 0', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <img src={item.image ? `http://localhost:8000${item.image}` : 'https://via.placeholder.com/50'} alt={item.name} style={{width: '50px', height: '50px', marginRight: '10px'}} />
            <span>{item.name}</span>
          </div>
          <div>
            <input
              type="number"
              value={item.quantity}
              min="1"
              max={item.stock} // Assuming stock info is on the item in cart
              onChange={(e) => updateQuantity(item.id, parseInt(e.target.value))}
              style={{width: '50px', marginRight: '10px'}}
            />
            <span>@ ${item.price} each</span>
          </div>
          <div>
            <span>Subtotal: ${(item.price * item.quantity).toFixed(2)}</span>
            <button onClick={() => removeFromCart(item.id)} style={{ marginLeft: '10px' }}>Remove</button>
          </div>
        </div>
      ))}
      <div style={{ marginTop: '20px', textAlign: 'right' }}>
        <h3>Total: ${getCartTotal()}</h3>
        {/* Link to checkout page will go here */}
        <Link to="/checkout" style={{ padding: '10px 20px', backgroundColor: 'green', color: 'white', textDecoration: 'none', borderRadius: '5px' }}>
          Proceed to Checkout
        </Link>
      </div>
    </div>
  );
};

export default CartPage;
