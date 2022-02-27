import api from "./api";
import TokenService from "./token.service";

class AuthService {
  login({ username, password }) {
    return api
      .post("/login", {
        username,
        password,
      })
      .then((response) => {
        console.log(response.data);
        user = {
          refresh_token: user.data.refresh_token,
        };
        if (response.data.access_token) {
          TokenService.setUser(user);
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
    return api.post("/register", {
      username,
      account_name,
      password,
    });
  }
}

export default new AuthService();
