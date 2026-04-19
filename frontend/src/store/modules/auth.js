import authApi from '@/api/auth';

const TOKEN_KEY = 'auth_token';

export default {
  namespaced: true,

  state: {
    token: localStorage.getItem(TOKEN_KEY) || null,
  },

  getters: {
    isAuthenticated: (state) => state.token !== null,
    token: (state) => state.token,
    username: (state) => {
      if (!state.token) return null;
      try {
        const payload = JSON.parse(atob(state.token.split('.')[1]));
        return payload.sub || null;
      } catch {
        return null;
      }
    },
  },

  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem(TOKEN_KEY, token);
    },
    clearToken(state) {
      state.token = null;
      localStorage.removeItem(TOKEN_KEY);
    },
  },

  actions: {
    async login({ commit }, { username, password }) {
      const response = await authApi.login(username, password);
      commit('setToken', response.data.token);
    },
    logout({ commit }) {
      commit('clearToken');
    },
  },
};
