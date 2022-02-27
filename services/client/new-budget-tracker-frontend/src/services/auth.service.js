import api from "./api";
import TokenService from "./token.service";

class AuthService {
  login({ username, password }) {
    return api
      .post("/auth-service/login", {
        username,
        password,
      })
      .then((response) => {
        if (response.data.access_token) {
          TokenService.setUser(response.data.refresh_token);
          TokenService.updateAccessToken(response.data.access_token);
        }
        return response.data;
      })
      .catch((err) => {
        console.log(err);
      });
  }

  logout() {
    TokenService.removeUser();
  }

  register({ username, account_name, password }) {
    return api.post("/auth-service/register", {
      username,
      account_name,
      password,
    });
  }

  refresh({ refresh_token }) {
    return api
      .post("/auth-service/refresh", {
        refresh_token,
      })
      .then((response) => {
        TokenService.updateLocalRefreshToken(response.data.refresh_token);
        TokenService.updateAccessToken(response.data.access_token);
      })
      .catch((err) => {
        console.log(err);
      });
  }
}

export default new AuthService();
