import axios from "axios";
import authHeader from "./auth-header";

const API_URL = "http://localhost:8001/api/v1/auth-service";
class UserService {
    getAuthStatus() {
        return axios.get(API_URL + '/status', { headers: authHeader()});
    }
}

export default new UserService();