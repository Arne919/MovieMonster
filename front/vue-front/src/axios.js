import axios from "axios";

const axiosInstance = axios.create({
  baseURL: "http://127.0.0.1:8000/api/v1", // Django API URL
  timeout: 10000, // 요청 시간 초과
  withCredentials: true, // 필요하면 사용
});

export default axiosInstance;
