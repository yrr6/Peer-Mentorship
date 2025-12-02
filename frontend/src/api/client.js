import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:4000/api/v1", // backend URL
});

// Example API calls
export const getPosts = () => api.get("/posts");
export const loginUser = (data) => api.post("/auth/login", data);
export const registerUser = (data) => api.post("/auth/register", data);

export default api;
