import axios from "axios";
const API_URL = "http://localhost:8001/api/v1/auth-service";
class AuthService {
    login(user) {
        return axios
            .post(
                API_URL + '/login', {
                    username: user.username,
                    password: user.password,
                }
            )
            .then(response => {
                if (response.data.access_token) {
                    localStorage.setItem('user', JSON.stringify(response.data));
                }
                return response.data;
            });
    }
    logout(user) {
        localStorage.removeItem('user')
    }
    register(user) {
        return axios.post(API_URL+'/register', {
            username: user.username,
            account_name: user.account_name,
            password: user.password
        });
    }
}

export default new AuthService