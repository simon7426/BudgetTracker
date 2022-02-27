import axiosInstance from "./api";
import { useAuthStore } from "../stores/useAuth";
import { storeToRefs } from "pinia";
import TokenService from "./token.service";

const values = useAuthStore();
const { access_token } = storeToRefs(values);

const setup = (store) => {
  axiosInstance.interceptors.request.use(
    (config) => {
      if (access_token) {
        config.headers["Authorization"] = "Bearer " + access_token;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );

  axiosInstance.interceptors.response.use(
    (res) => {
      return res;
    },
    async (err) => {
      const originalConfig = err.config;
      if (originalConfig.url !== "/login" && err.response) {
        if (err.response.status == 401 && !originalConfig._retry) {
          originalConfig._retry = true;

          try {
            const rs = await axiosInstance.post("/refresh", {
              refresh_token: TokenService.getLocalRefreshToken(),
            });
            const { access_token } = rs.data.access_token;
            const { refresh_token } = rs.data.refresh_token;
            values.setToken(access_token);
            TokenService.updateLocalRefreshToken(refresh_token);

            return axiosInstance(originalConfig);
          } catch (_error) {
            return Promise.reject(_error);
          }
        }
      }

      return Promise.reject(err);
    }
  );
};

export default setup;
