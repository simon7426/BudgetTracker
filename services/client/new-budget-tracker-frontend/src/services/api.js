import axios from "axios";

const instance = axios.create({
  baseURL: "http://localhost:8001/api/v1/auth-service",
  headers: {
    "Content-Type": "application-json",
  },
});

export default instance;
