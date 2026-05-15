import axios from "axios";

const api = axios.create({
  baseURL: "http://192.168.100.201:8000/api",
  // baseURL: "http://127.0.0.1:8000/api",
});

// api.interceptors.request.use((config) => {
//   const token = localStorage.getItem("access");

//   if (token) {
//     config.headers.Authorization = `Bearer ${token}`;
//   }

//   return config;
// });

export default api;