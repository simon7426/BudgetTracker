import { useAuthStore } from "../stores/useAuth"

class TokenService {

  getAccessToken() {
    const values = useAuthStore();
    const { access_token } = values;
    return access_token.value
  }

  getLocalRefreshToken() {
    const user = JSON.parse(localStorage.getItem("user"));
    return user?.refresh_token;
  }

  updateLocalRefreshToken(token) {
    let user = JSON.parse(localStorage.getItem("user"));
    user.refresh_token = token;
    localStorage.setItem("user", JSON.stringify(user));
  }

  updateAccessToken(token){
    const values = useAuthStore();
    values.setToken(token)
  }

  getUser() {
    return JSON.parse(localStorage.getItem("user"));
  }

  setUser(refresh_token) {
    const user = {
      refresh_token: refresh_token,
    };
    localStorage.setItem("user", JSON.stringify(user));
  }

  removeUser() {
    const values = useAuthStore();
    values.removeToken();
    localStorage.removeItem("user");
  }
}

export default new TokenService();
