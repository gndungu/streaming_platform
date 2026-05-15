import { useState } from "react";
import { loginUser } from "../api/auth";
import ErrorDialog from "../components/ErrorDialog";
import { validateForm } from "../utils/validator";
import { Link } from "react-router-dom";
import BackButton from "../components/BackButton";
import bg from "../assets/cinemaroom.jpg";

export default function LoginPage() {

  const [form, setForm] = useState({
    username: "",
    password: ""
  });

  const [error, setError] = useState("");
  const [errors, setErrors] = useState({});
  

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const validationErrors = validateForm(form);
    setErrors(validationErrors);

    if (Object.keys(validationErrors).length > 0) return;

    try {
      const res = await loginUser(form);

      localStorage.setItem("user", JSON.stringify(res.data.user));

    //   alert("Welcome " + res.data.user.username);

      window.location.href = "/";

    } catch (err) {
      setError(
        err.response?.data?.error || "Login failed"
      );
    }
  };

  return (
    <div className="h-screen flex items-center justify-center relative text-white">

  {/* 🌑 Background */}
  <div
    className="absolute inset-0 bg-cover bg-center"
    style={{
      backgroundImage: `url(${bg})`
    }}
  ></div>

  {/* Dark overlay */}
  <div className="absolute inset-0 bg-black/70"></div>
    <div className="absolute top-6 left-6 z-20">
        <BackButton to="/" label="Back to Home" />
    </div>
  {/* 🧾 Login Card */}
  <div className="relative z-10 bg-black/80 backdrop-blur-md p-8 rounded-xl w-96 shadow-2xl">
  
    
    <h2 className="text-3xl font-bold mb-6 text-center">
      Login
    </h2>

    <input
      name="username"
      placeholder="Username"
      className="w-full p-3 mb-3 rounded bg-gray-800 text-white placeholder-gray-400 outline-none focus:ring-2 focus:ring-green-600"
      onChange={handleChange}
    />
    {errors.username && (
        <p className="text-red-400 text-sm mb-2">
            {errors.username}
        </p>
        )}

    <input
      name="password"
      type="password"
      placeholder="Password"
      className="w-full p-3 mb-4 rounded bg-gray-800 text-white placeholder-gray-400 outline-none focus:ring-2 focus:ring-green-600"
      onChange={handleChange}
    />
    {errors.password && (
        <p className="text-red-400 text-sm mb-2">
            {errors.password}
        </p>
        )}

    <button
      onClick={handleSubmit}
      className="w-full bg-green-600 hover:bg-green-700 transition p-3 rounded font-semibold"
    >
      Login
    </button>

    <p className="text-sm text-gray-400 mt-4 text-center">
    Don’t have an account?{" "}
    
    <Link
        to="/register"
        className="text-green-500 hover:text-green-400 font-semibold"
    >
        Register
    </Link>
    </p>

  </div>

  <ErrorDialog
        message={error}
        onClose={() => setError("")}
      />

</div>
  );
}