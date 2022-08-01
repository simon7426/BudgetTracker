import axios from "axios";
import router from "../router";
import { useAuthStore } from "../stores/useAuth";
import authService from "./auth.service";
import tokenService from "./token.service";

const instance = axios.create({
  // baseURL: "/api/v1",
  // baseURL: "https://tracker.simonislam.com"+"/api/v1",
  baseURL: "http://hello.world" + "/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

instance.interceptors.request.use(
  (config) => {
    const store = useAuthStore();
    if (store.access_token) {
      config.headers["Authorization"] = "Bearer " + store.access_token;
    }
    return config;
  },
  (error) => {
    console.log(error);
  }
);

instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (err) => {
    console.log("In response error");
    const originalConfig = err.config;
    if (
      err.response &&
      err.response.status == 401 &&
      originalConfig.url !== "/auth-service/refresh" &&
      originalConfig.url !== "/auth-service/login" &&
      !originalConfig._retry
    ) {
      originalConfig._retry = true;
      try {
        const refresh_token = tokenService.getLocalRefreshToken();
        console.log(refresh_token);
        authService
          .refresh(refresh_token)
          .then((response) => {
            console.log(response);
            return instance(originalConfig);
          })
          .catch((err) => {
            console.log("Error fetching refresh token");
            console.log(err);
            router.push({ name: "Login" });
          });
      } catch (_error) {
        console.log(_error);
      }
    }
  }
);

export default instance;
