import axiosInstance from "./api";
import TokenService from "./token.service";


const setup = (store) => {
  axiosInstance.interceptors.request.use(
    (config) => {
      
      if (store.access_token) {
        console.log(config)
        config.headers["Authorization"] = "Bearer " + store.access_token;
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
      if (originalConfig.url !== "/auth-service/login" && err.response) {
        if (err.response.status == 401 && !originalConfig._retry) {
          originalConfig._retry = true;

          try {
            const rs = await axiosInstance.post("/auth-service/refresh", {
              refresh_token: TokenService.getLocalRefreshToken(),
            }).then((rs)=>{
              const { access_token } = rs.data.access_token;
              const { refresh_token } = rs.data.refresh_token;
              TokenService.updateAccessToken(access_token)
              TokenService.updateLocalRefreshToken(refresh_token);
              return axiosInstance(originalConfig);
            });
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
