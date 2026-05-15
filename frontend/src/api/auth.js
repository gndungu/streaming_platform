import api from "./axios";
import { getCookie } from "../utils/cookies";

export const registerUser = (data) => {
  const csrfToken = getCookie("csrftoken");

  return api.post("/accounts/register/", data, {
    withCredentials: true,
    headers: {
      "X-CSRFToken": csrfToken,
      "Content-Type": "application/json",
    },
  });
};

// export const loginUser = async (data) => {
//   const res = await api.post("/accounts/login/", data);
  
//   localStorage.setItem("access", res.data.tokens.access);
//   localStorage.setItem("refresh", res.data.tokens.refresh);

//   return res.data;
// };

export const loginUser = (data) => {
  const csrfToken = getCookie("csrftoken");

  return api.post("/accounts/login/", data, {
    withCredentials: true,
    headers: {
      "X-CSRFToken": csrfToken,
      "Content-Type": "application/json",
    },
  });
};

export const logoutUser = () =>
  api.post("/accounts/logout/");