<template>
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-12 col-sm-8 col-md-6 col-lg-4 my-5">
        <h2 class="mb-4 text-center">Login</h2>
        <form @submit.prevent="submit">
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              id="username"
              type="text"
              class="form-control"
              v-model="username"
              placeholder="Enter your username"
              :disabled="loading"
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              id="password"
              type="password"
              class="form-control"
              v-model="password"
              placeholder="Enter your password"
              :disabled="loading"
            />
          </div>
          <div class="mb-3" v-if="error">
            <div class="alert alert-danger p-2" role="alert">{{ error }}</div>
          </div>
          <div class="d-grid">
            <button
              type="submit"
              class="btn btn-dark d-inline-flex justify-content-center align-items-center"
              :disabled="loading || !canSubmit"
            >
              <template v-if="loading">
                Logging in…
                <span class="spinner-border spinner-border-sm ms-1" role="status" aria-hidden="true"></span>
              </template>
              <template v-else>Login</template>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Login',
  data() {
    return { username: '', password: '', loading: false, error: null };
  },
  computed: {
    canSubmit() {
      return this.username.length > 0 && this.password.length > 0;
    },
  },
  methods: {
    async submit() {
      this.loading = true;
      this.error = null;
      try {
        await this.$store.dispatch('auth/login', { username: this.username, password: this.password });
        this.$router.push('/');
      } catch (err) {
        if (err.response && err.response.status === 401) {
          this.error = 'Invalid username or password';
        } else {
          this.error = 'Something went wrong';
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
