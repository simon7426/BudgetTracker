import { defineStore } from "pinia";
import authService from "../services/auth.service";

export const useAuthStore = defineStore("auth", {
  state: () => ({
    access_token: null,
  }),
  getters: {
      isLoggedIn() {
         return this.access_token !== null
      }
  },
  actions: {
    logout() {
      this.access_token = null;
    },
    setToken(access_token) {
      this.access_token = access_token;
    },
    removeToken() {
      this.access_token = null;
    }
  },
});
