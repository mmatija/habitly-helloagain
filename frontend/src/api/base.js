import axios from 'axios';
import config from '@/config';

const instance = axios.create({
  baseURL: config.apiUri,
  headers: {
    Accept: 'application/json',
  },
});

// Request interceptor to append jwt token from localStorage on every request
instance.interceptors.request.use(function (config) {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default instance;
