import axios from "axios";

const instance = axios.create({
  baseURL: "http://127.0.0.1:8000/api", // Django API URL
  withCredentials: true, // 필요하면 사용 (로그인 인증 등)
});

export default instance;
