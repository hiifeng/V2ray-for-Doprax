import axios from 'axios';

const API_URL = '/api/store'; // Assuming proxy is set up or same domain

export const getProducts = () => {
  return axios.get(`${API_URL}/products/`);
};

export const getProductById = (id) => {
  return axios.get(`${API_URL}/products/${id}/`);
};

// Add other API functions here (categories, orders, auth) as needed
