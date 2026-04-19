import axios from 'axios';
import api_config from '../../api_config.json';

const instance = axios.create({
  baseURL: api_config.api_uri,
  headers: {
    Accept: 'application/json',
  },
});

export default {
  login(username, password) {
    return instance.post('login/', { username, password });
  },
};
