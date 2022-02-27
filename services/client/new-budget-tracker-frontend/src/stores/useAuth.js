import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    access_token: null,
  }),
  getters: {
      isLoggedIn() {
          this.access_token !== null
      }
  },
  actions: {
    logout() {
      this.access_token = null;
    },
    setToken(access_token) {
      this.access_token = access_token;
    },
  },
});
