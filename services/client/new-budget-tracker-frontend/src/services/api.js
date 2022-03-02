import axios from "axios";

const instance = axios.create({
  baseURL: "http://hello.world/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

export default instance;
