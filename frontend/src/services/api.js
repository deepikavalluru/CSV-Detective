import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const investigateCSV = async (file) => {
  const formData = new FormData();

  formData.append("file", file);

  const response = await api.post("/api/investigate", formData);

  return response.data;
};